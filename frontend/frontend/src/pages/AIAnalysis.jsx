import { useState } from "react";
import api from "../service/api";

function AIAnalysis() {

    const [analysis, setAnalysis] = useState("");
    const [anomalies, setAnomalies] = useState([]);

    const [loadingAnalysis, setLoadingAnalysis] = useState(false);
    const [loadingAnomalies, setLoadingAnomalies] = useState(false);

    const [error, setError] = useState("");

    const handleAnalyze = async () => {

        try {

            setLoadingAnalysis(true);
            setError("");

            const response = await api.post(
                "/ai/analyze"
            );

            setAnalysis(
                response.data.analysis
            );

        } catch (error) {

            console.error(
                "AI analysis error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Unable to generate AI analysis."
            );

        } finally {

            setLoadingAnalysis(false);
        }
    };


    const handleAnomalies = async () => {

        try {

            setLoadingAnomalies(true);
            setError("");

            const response = await api.post(
                "/ai/anomalies"
            );

            setAnomalies(
                response.data.anomalies || []
            );

        } catch (error) {

            console.error(
                "Anomaly error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Unable to detect unusual expenses."
            );

        } finally {

            setLoadingAnomalies(false);
        }
    };


    return (
        <div className="ai-page">

            <div className="ai-header">

                <h1>
                    ✨ AI Financial Assistant
                </h1>

                <p>
                    Get intelligent insights
                    from your expenses.
                </p>

            </div>


            {error && (
                <div className="error">
                    {error}
                </div>
            )}


            {/* ANALYSIS */}

            <div className="ai-card">

                <h2>
                    📊 Expense Analysis
                </h2>

                <p>
                    Let AI analyze your spending
                    patterns and provide useful
                    insights.
                </p>

                <button
                    onClick={handleAnalyze}
                    disabled={loadingAnalysis}
                >
                    {loadingAnalysis
                        ? "Analyzing..."
                        : "Analyze My Expenses"}
                </button>

                {analysis && (
                    <div className="ai-result">

                        <h3>
                            AI Analysis
                        </h3>

                        <div className="analysis-text">
                            {analysis}
                        </div>

                    </div>
                )}

            </div>


            {/* ANOMALIES */}

            <div className="ai-card">

                <h2>
                    ⚠️ Unusual Spending
                </h2>

                <p>
                    Find potentially unusual
                    expenses in your spending.
                </p>

                <button
                    onClick={handleAnomalies}
                    disabled={loadingAnomalies}
                >
                    {loadingAnomalies
                        ? "Checking..."
                        : "Check Unusual Expenses"}
                </button>


                {anomalies.length > 0 && (

                    <div className="anomaly-list">

                        <h3>
                            Potentially Unusual
                            Expenses
                        </h3>

                        {anomalies.map(
                            (anomaly, index) => (

                                <div
                                    className="anomaly-card"
                                    key={index}
                                >

                                    <strong>
                                        {anomaly.category}
                                    </strong>

                                    <span>
                                        ₹
                                        {Number(
                                            anomaly.amount
                                        ).toFixed(2)}
                                    </span>

                                    <p>
                                        {anomaly.reason}
                                    </p>

                                </div>

                            )
                        )}

                    </div>

                )}

                {anomalies.length === 0 &&
                    !loadingAnomalies && (
                        <p className="no-anomalies">
                            No unusual expenses
                            detected.
                        </p>
                    )}

            </div>

        </div>
    );
}

export default AIAnalysis;