import { useEffect, useState } from "react";
import api from "../service/api";

function Profile() {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        const getProfile = async () => {

            try {

                const response = await api.get(
                    "/users/me"
                );

                setUser(response.data);

            } catch (error) {

                console.error(
                    "Profile error:",
                    error
                );

                setError(
                    "Unable to load profile."
                );

            } finally {

                setLoading(false);
            }
        };

        getProfile();

    }, []);

    if (loading) {
        return (
            <div className="profile-page">
                Loading profile...
            </div>
        );
    }

    if (error) {
        return (
            <div className="profile-page">
                <div className="error">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="profile-page">

            <div className="profile-card">

                <div className="profile-avatar">
                    {user?.name
                        ?.charAt(0)
                        ?.toUpperCase()}
                </div>

                <h1>
                    {user?.name}
                </h1>

                <p className="profile-email">
                    {user?.email}
                </p>

                <div className="profile-details">

                    <div>
                        <span>User ID</span>
                        <strong>
                            {user?.id}
                        </strong>
                    </div>

                    <div>
                        <span>Account Status</span>
                        <strong>
                            {user?.account_status
                                ? "Active"
                                : "Inactive"}
                        </strong>
                    </div>

                </div>

            </div>

        </div>
    );
}

export default Profile;