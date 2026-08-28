import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def analyze_expenses(expense_data: str) -> str:

    prompt = f"""
You are an AI financial assistant.

Analyze ONLY the expense data provided below.

IMPORTANT RULES:
- Do not invent any information.
- Do not assume an expense is essential or non-essential unless the data clearly indicates it.
- Do not change or reinterpret expense descriptions.
- Use the exact amounts provided.
- If something cannot be determined from the data, say so.
- Do not give financial or investment advice.
- Keep the analysis concise.

Expense data:
{expense_data}

Provide:

1. Total spending
2. Highest spending category
3. Spending patterns based only on the data
4. Potential areas to reduce spending
5. Three practical suggestions
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text



def analyze_anomalies(anomaly_data: str) -> str:

    prompt = f"""
You are an AI financial assistant.

Analyze the potentially unusual expenses provided below.

IMPORTANT RULES:
- Use ONLY the provided information.
- Do not invent amounts or expenses.
- Do not claim something is definitely unusual unless the data supports it.
- Explain why each expense may be unusual.
- Keep the explanation simple and concise.
- Do not give investment or financial advice.

Potentially unusual expenses:
{anomaly_data}

For each expense, provide a short explanation.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


