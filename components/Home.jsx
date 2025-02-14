// Home.js
import React, { useState } from "react";
import "./Home.css";
import Button from "./sexy-button";
import ProgressBar from "./progress-bar";
import ProgressBar2 from "./progress-bar2";
import ProgressBar3 from "./progress-bar3";

import ThoughtContainer from "./reasonContainer";

function Home() {
    const [mood, setMood] = useState({
        Sadness: 0,
        Anxiety: 0,
        Happiness: 0,
        Explanation: "No analysis yet."
    });

    const handleAnalyze = () => {
        const loginWindow = window.open(
            "http://localhost:5000/",
            "Spotify Login",
            "width=600,height=800"
        );

        const handleMessage = async (event) => {

            if (event.data === "spotifyAuthSuccess") {
                console.log("Received login success message from popup");
                // Remove the listener once received
                window.removeEventListener("message", handleMessage);

                try {
                    const response = await fetch("http://localhost:5000/analyze", {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        credentials: "include" // Include cookies for session handling
                    });
                    const data = await response.json();

                    if (data.error) {
                        alert(data.error);
                        return;
                    }


                    console.log("Analysis data received:", data);


                    setMood({
                        Sadness: data.Sadness,
                        Anxiety: data.Anxiety,
                        Happiness: data.Happiness,
                        Explanation: data.Explanation
                    });
                } catch (error) {
                    console.error("Error fetching analysis data:", error);
                }
            }
        };

        window.addEventListener("message", handleMessage, false);
    };

    return (
        <div className="homeContainer">
            <header className="header">
                <div className="logo">Expressify</div>
            </header>
            <h1>
                Analyze your emotions from Spotify utilizing AI. Log in to get started.
            </h1>
            <Button onClick={handleAnalyze}>Connect Spotify</Button>
            <ProgressBar percentage={mood.Sadness} label="Sadness" />
            <ProgressBar2 percentage={mood.Anxiety} label="Anxiety" />
            <ProgressBar3 percentage={mood.Happiness} label="Happiness" />
            <ThoughtContainer text={mood.Explanation} />
        </div>
    );
}

export default Home;