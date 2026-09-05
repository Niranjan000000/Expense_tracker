import { createContext, useContext, useState } from "react";
import api from "../service/api.js";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

    const login = async (email, password) => {
        setLoading(true);

        try {
            const response = await api.post("/auth/login", {
                email: email,
                password: password,
            });

            const token = response.data.access_token;

            localStorage.setItem(
                "access_token",
                token
            );

            const userResponse = await api.get(
                "/users/me"
            );

            setUser(userResponse.data);

            return true;

        } catch (error) {
            console.error("Login error:",error);
            console.error("STATUS:", error.response?.status);
            console.error("DATA:", error.response?.data);


            return false;

        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem(
            "access_token"
        );

        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}