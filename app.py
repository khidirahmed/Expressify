import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai
import os
from flask import Flask, request, redirect, session, jsonify, make_response, Response
from dotenv import load_dotenv
from flask_cors import CORS
import flask_session

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = "SpotifyLogin"


CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Allow cross-site cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = "spotify_"
app.config['SESSION_FILE_DIR'] = "./flask_session"


flask_session.Session(app)


sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played"
)

app.secret_key = "HelloWorlds"

@app.route('/')
def login():
    if session.get("token_info"):
        html = """
        <html>
          <head>
            <script type="text/javascript">
              window.opener.postMessage("spotifyAuthSuccess", "*");
              // Removed auto-close so the user can close manually
            </script>
          </head>
          <body>
            Already logged in. Please close this window manually.
          </body>
        </html>
        """
        return Response(html, mimetype='text/html')
    else:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization code from the URL parameters
    code = request.args.get("code")
    if not code:
        return "Authorization code not found", 400

    try:
        # Retrieve the token from the cache instead of exchanging the code
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            return "Token not found in cache. Please authenticate again.", 400

        # Store the token in the session
        session["token_info"] = token_info
        session.modified = True  # Ensure Flask knows the session was changed

        # Debug prints to confirm storage
        print("Token successfully stored in session:")
        print(token_info)
        print("Current session contents:", dict(session))

        # Return an HTML page that notifies the parent window of success
        html = """
        <html>
          <head>
            <script type="text/javascript">
              window.opener.postMessage("spotifyAuthSuccess", "*");
            </script>
          </head>
          <body>
            <h1>Login Successful!</h1>
            <p>You can now close this window and return to the app.</p>
          </body>
        </html>
        """
        return Response(html, mimetype='text/html')
    except Exception as e:
        print("Error during token retrieval and storage:", str(e))
        return "Error during Spotify authentication", 500

def get_spotify_client():
    print("Current session contents:", dict(session))
    print("Session keys:", list(session.keys()))
    token_info = session.get('token_info')

    print("Token info in get_spotify_client:", token_info)

    if not token_info:
        print("Error: No token_info in session")
        return None
    try:
        is_expired = sp_oauth.is_token_expired(token_info)
        print(f"Is token expired? {is_expired}")

        if is_expired:
            print("Token expired, attempting refresh...")
            if "refresh_token" not in token_info:
                print("Error: No refresh token found in token_info")
                return None

            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info
            print("Token refreshed successfully:", token_info)

        client = spotipy.Spotify(auth=token_info["access_token"])
        client.current_user()
        return client

    except spotipy.SpotifyException as e:
        print(f"Spotify API Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_spotify_client: {str(e)}")
        return None

def get_recent_tracks():
    sp = get_spotify_client()
    if not sp:
        print("Error: Spotify client is None (token missing or invalid)")
        return None

    try:
        results = sp.current_user_recently_played(limit=10)
        tracks = [
            f"{item['track']['name']} by {item['track']['artists'][0]['name']}"
            for item in results["items"]
        ]
        print("Tracks retrieved:", tracks)
        return tracks
    except Exception as e:
        print("Error fetching tracks:", str(e))
        return None

def analyze_mood_with_ai(tracks):
    tracks_text = "\n".join(tracks)
    prompt = f"""
    Based on the following recently played songs, analyze the user's mood in terms of Sadness, Anxiety, and Happiness.
    Give three percentage scores (which add to 100%) and a brief explanation.

    Songs:
    {tracks_text}

    Respond with a JSON object in the following format:
    {{
      "Sadness": <number>,
      "Anxiety": <number>,
      "Happiness": <number>,
      "Explanation": "<string>"
    }}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        mood_data = json.loads(content)
        return mood_data
    except Exception as e:
        print("Error analyzing mood with AI:", str(e))
        return None

@app.route('/analyze')
def analyze_mood():
    print("Starting mood analysis...")
    tracks = get_recent_tracks()
    if not tracks:
        return make_response(jsonify({"error": "Please log into Spotify again to analyze your mood."}), 400)
    mood_data = analyze_mood_with_ai(tracks)
    if not mood_data:
        return make_response(jsonify({"error": "Error analyzing mood. Try again later."}), 500)
    print("Final mood data:", mood_data)
    return jsonify(mood_data)


if __name__ == "__main__":
    app.run(debug=True)