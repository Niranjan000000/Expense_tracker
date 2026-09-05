import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {

    const navigate = useNavigate();
    const location = useLocation();

    const { user, logout } = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <nav className="navbar">

            <div
                className="navbar-logo"
                onClick={() => navigate("/dashboard")}
            >
                💰 Expense Tracker
            </div>

            <div className="navbar-links">

                <button
                    className={
                        location.pathname === "/dashboard"
                            ? "nav-active"
                            : ""
                    }
                    onClick={() =>
                        navigate("/dashboard")
                    }
                >
                    Dashboard
                </button>

                <button
                    className={
                        location.pathname === "/expenses"
                            ? "nav-active"
                            : ""
                    }
                    onClick={() =>
                        navigate("/expenses")
                    }
                >
                    Expenses
                </button>

                <button
                    className={
                        location.pathname === "/ai"
                            ? "nav-active"
                            : ""
                    }
                    onClick={() =>
                        navigate("/ai")
                    }
                >
                    🤖 AI
                </button>

                <button
                    className={
                        location.pathname === "/profile"
                            ? "nav-active"
                            : ""
                    }
                    onClick={() =>
                        navigate("/profile")
                    }
                >
                    Profile
                </button>

                <button
                    className="logout-button"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </div>

            {user && (
                <div className="navbar-user">
                    {user.name}
                </div>
            )}

        </nav>
    );
}

export default Navbar;