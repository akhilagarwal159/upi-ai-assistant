import streamlit as st
import json
import pandas as pd
import plotly.express as px

# Load data
with open("transactions.json") as f:
    data = json.load(f)


def ask_ai(user_query):
    query = user_query.lower()

    if "fail" in query:
        failed = [t for t in data if t["status"] == "FAILED"]

        if not failed:
            return "No failed transactions found."

        reasons = set(t.get("reason", "UNKNOWN") for t in failed)

        response = "Some transactions failed due to: "
        response += ", ".join(reasons)
        response += ". "

        

        return response

    elif "spend" in query:
        total = sum(t["amount"] for t in data if t["status"] == "SUCCESS")
        return f"You spent a total of ₹{total} in successful transactions."

    else:
        return "I can help you with transaction failures and spending insights."


# UI
st.title("💳 UPI AI Assistant")

st.write("### 💡 Try asking:")

suggestions = [
    "Why did my transaction fail?",
    "How much did I spend?",
    "Show my spending insights",
    "Help me understand failed payments"
]

selected_question = st.selectbox("Choose a question or type your own:", [""] + suggestions)

user_input = st.text_input("Question:", value=selected_question)

if st.button("Submit") and user_input:
    response = ask_ai(user_input)
    st.write("### 🤖 Answer:")
    st.write(response)

st.write("## 📊 Spending Insights")

total_spent = sum(t["amount"] for t in data if t["status"] == "SUCCESS")

st.write(f"💰 Total Spent: ₹{total_spent}")

# Merchant-wise spending
merchant_spend = {}
for t in data:
    if t["status"] == "SUCCESS":
        merchant_spend[t["merchant"]] = merchant_spend.get(t["merchant"], 0) + t["amount"]


df = pd.DataFrame(list(merchant_spend.items()), columns=["Merchant", "Amount"])
df = df.sort_values(by="Amount", ascending=False)

st.markdown("### 🛍️ **Spend Analysis Dashboard**")
df = pd.DataFrame(list(merchant_spend.items()), columns=["Merchant", "Amount"])
df = df.sort_values(by="Amount", ascending=False)


fig = px.bar(
    df,
    x="Merchant",
    y="Amount",
    text="Amount",
    title="Spend by Merchant"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Merchant",
    yaxis_title="Amount (₹)",
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig)