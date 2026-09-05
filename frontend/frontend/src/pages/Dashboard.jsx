import { useEffect, useState } from "react";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid
} from "recharts";

import { useNavigate } from "react-router-dom";

import api from "../service/api";


const PIE_COLORS = [
    "#2563eb",
    "#16a34a",
    "#f59e0b",
    "#dc2626",
    "#7c3aed",
    "#0891b2"
];


function Dashboard() {

    const navigate = useNavigate();

    const [summary, setSummary] = useState(null);

    const [categoryData, setCategoryData] = useState([]);

    const [monthlyData, setMonthlyData] = useState([]);

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        const loadDashboard = async () => {

            try {

                const [
                    userResponse,
                    summaryResponse,
                    categoryResponse,
                    monthlyResponse
                ] = await Promise.all([

                    api.get("/users/me"),

                    api.get("/expenses/summary"),

                    api.get("/expenses/summary/category"),

                    api.get("/expenses/summary/monthly")

                ]);


                setUser(
                    userResponse.data
                );



                setSummary(
                    summaryResponse.data
                );



                const formattedCategoryData =
                    categoryResponse.data.map(
                        (item) => ({

                            name: item.category,

                            value: Number(
                                item.total
                            )

                        })
                    );


                console.log(
                    "FORMATTED CATEGORY DATA:",
                    formattedCategoryData
                );


                setCategoryData(
                    formattedCategoryData
                );



                const formattedMonthlyData =
                    monthlyResponse.data.map(
                        (item) => ({

                            ...item,

                            total: Number(
                                item.total
                            )

                        })
                    );


                setMonthlyData(
                    formattedMonthlyData
                );


            } catch (error) {

                console.error(
                    "Dashboard error:",
                    error
                );


                console.error(
                    "Status:",
                    error.response?.status
                );


                console.error(
                    "Data:",
                    error.response?.data
                );


                setError(
                    "Unable to load dashboard data."
                );


            } finally {

                setLoading(false);

            }

        };


        loadDashboard();

    }, []);




    if (loading) {

        return (

            <div className="dashboard-loading">

                Loading dashboard...

            </div>

        );

    }



    if (error) {

        return (

            <div className="dashboard-error">

                {error}

            </div>

        );

    }


    return (

        <div className="dashboard">



            <div className="dashboard-header">

                <div>

                    <h1>
                       Expense Tracker Dashboard
                    </h1>


                    <p>

                        Welcome back,{" "}

                        <strong>
                            {user?.name}
                        </strong>{" "}

                        👋

                    </p>

                </div>


                <div className="dashboard-actions">

                    <button
                        className="expenses-button"
                        onClick={() =>
                            navigate("/expenses")
                        }
                    >
                        ⚖️ Manage Expenses
                    </button>


                    <button
                        className="ai-button"
                        onClick={() =>
                            navigate("/ai")
                        }
                    >
                        ✨ AI Insights
                    </button>

                </div>

            </div>



            <div className="stats-grid">



                <div className="stat-card">

                    <p>
                        Total Spending
                    </p>


                    <h2>

                        ₹

                        {Number(
                            summary?.total_amount || 0
                        ).toFixed(2)}

                    </h2>

                </div>



                <div className="stat-card">

                    <p>
                        Total Expenses
                    </p>


                    <h2>

                        {summary?.total_expenses || 0}

                    </h2>

                </div>


                {/* CATEGORIES */}

                <div className="stat-card">

                    <p>
                        Categories
                    </p>


                    <h2>

                        {categoryData.length}

                    </h2>

                </div>

            </div>


            {/* CHARTS */}

            <div className="charts-grid">


                <div className="chart-card">

                    <h2>
                        Spending by Category
                    </h2>


                    {categoryData.length === 0 ? (

                        <p>
                            No category data available.
                        </p>

                    ) : (

                        <ResponsiveContainer
                            width="100%"
                            height={350}
                        >

                            <PieChart>

                                <Pie

                                    data={categoryData}

                                    dataKey="value"

                                    nameKey="name"

                                    cx="50%"

                                    cy="50%"

                                    outerRadius={110}

                                    label

                                >

                                    {categoryData.map(
                                        (entry, index) => (

                                            <Cell
                                                key={
                                                    `cell-${index}`
                                                }
                                                fill={
                                                    PIE_COLORS[
                                                        index %
                                                        PIE_COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )}

                                </Pie>


                                <Tooltip
                                    formatter={(value) =>
                                        `₹${Number(
                                            value
                                        ).toFixed(2)}`
                                    }
                                />


                                <Legend />

                            </PieChart>

                        </ResponsiveContainer>

                    )}

                </div>


                <div className="chart-card">

                    <h2>
                        Monthly Spending
                    </h2>


                    {monthlyData.length === 0 ? (

                        <p>
                            No monthly data available.
                        </p>

                    ) : (

                        <ResponsiveContainer
                            width="100%"
                            height={350}
                        >

                            <BarChart
                                data={monthlyData}
                            >

                                <CartesianGrid />

                                <XAxis
                                    dataKey="month"
                                />

                                <YAxis />


                                <Tooltip
                                    formatter={(value) =>
                                        `₹${Number(
                                            value
                                        ).toFixed(2)}`
                                    }
                                />


                                <Bar
                                    dataKey="total"
                                    fill="#2563eb"
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    )}

                </div>

            </div>

        </div>

    );

}


export default Dashboard;