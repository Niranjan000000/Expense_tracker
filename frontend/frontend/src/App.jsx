import {
    BrowserRouter,
    Routes,
    Route
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";

import Login from "./pages/Login";
import Register from "./pages/Register";

import ProtectedRoute from "./component/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Expenses from "./pages/Expense";
import AIAnalysis from "./pages/AIAnalysis";
import Navbar from "./component/Navbar";
import Profile from "./pages/Profile";

function App() {

    return (
        <BrowserRouter>

            <AuthProvider>

                <Routes>

                    <Route
                        path="/"
                        element={
                            <Login />
                        }
                    />

                    <Route
                        path="/login"
                        element={
                            <Login />
                        }
                    />

                    <Route
                        path="/register"
                        element={
                            <Register />
                        }
                    />

                    <Route
                        path="/dashboard"
                         element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                     }
                    />
                    <Route
                         path="/expenses"
                         element={
                             <ProtectedRoute>
                                 <Expenses />
                            </ProtectedRoute>
                     }
                    />

                    <Route
                        path="/ai"
                        element={
                            <ProtectedRoute>
                                <AIAnalysis />
                            </ProtectedRoute>
                     }
                    />
                    <Route
                         path="/expenses"
                        element={
                             <ProtectedRoute>
                                    <Navbar />
                                    <Expenses />
                            </ProtectedRoute>
                     }
                    />

                    <Route
                    path="/ai"
                    element={
                        <ProtectedRoute>
                            <Navbar />
                            <AIAnalysis />
                        </ProtectedRoute>
                     }
                    />


                    <Route
                        path="/profile"
                        element={
                            <ProtectedRoute>
                                 <Navbar />
                                <Profile />
                            </ProtectedRoute>
                     }
                    />

                </Routes>

            </AuthProvider>

        </BrowserRouter>
    );
}

export default App;