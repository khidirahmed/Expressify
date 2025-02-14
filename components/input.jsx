import { useState } from "react";

function Input() {
    const [username, setUsername] = useState("");

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <label htmlFor="username" style={{ fontSize: "30px", fontWeight: "bold" }}>
                Username:
            </label>
            <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Type your username..."
                style={{
                    marginLeft: "10px",
                    padding: "12px",
                    fontSize: "20px",
                    width: "220px",
                    height: "30px",
                    borderRadius: "10px",
                    border: "2px solid #000",
                }}
            />
            <p style={{ marginTop: "10px", fontSize: "18px", marginBottom: "30px"}}>
                Username @<strong>{username}</strong>
            </p>
        </div>
    );
}

export default Input;