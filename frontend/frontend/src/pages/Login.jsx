import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const { login, loading } = useAuth();

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        setError("");

        const success = await login(
            email,
            password
        );

        if (success) {
            navigate("/dashboard");
        } else {
            setError(
                "Invalid email or password"
            );
        }
    };

    return (
        <div className="auth-container">

            <div className="auth-card">
                <h1>Expense Tracker Login</h1>
                <br></br>
                <h1>Welcome Back</h1>

                <p>
                    Login to your expense tracker
                </p>

                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}

                <form
                    onSubmit={handleSubmit}
                >

                    <label>Email</label>

                    <input
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        required
                    />

                    <label>Password</label>

                    <input
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                        required
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Logging in..."
                            : "Login"}
                    </button>

                </form>

                <p>
                    Don't have an account?
                    {" "}
                    <a href="/register">
                        Register
                    </a>
                </p>

            </div>

        </div>
    );
}

export default Login;