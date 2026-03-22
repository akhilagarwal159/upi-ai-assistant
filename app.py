import json

# Load transaction data
with open("transactions.json") as f:
    data = json.load(f)


def ask_ai(user_query):
    query = user_query.lower()

    # Case 1: Failure related
    if "fail" in query:
        failed = [t for t in data if t["status"] == "FAILED"]

        if not failed:
            return "No failed transactions found."

        reasons = set(t.get("reason", "UNKNOWN") for t in failed)

        response = "Some transactions failed due to: "
        response += ", ".join(reasons)
        response += ". "

        response += "Suggested actions: "

        if "BANK_SERVER_DOWN" in reasons:
            response += "Try again after some time. "
        if "INSUFFICIENT_BALANCE" in reasons:
            response += "Check your account balance. "

        return response

    # Case 2: Spending related
    elif "spend" in query:
        total = sum(t["amount"] for t in data if t["status"] == "SUCCESS")
        return f"You spent a total of ₹{total} in successful transactions."

    # Default response
    else:
        return "I can help you with transaction failures, spending, and insights."


# CLI loop
while True:
    query = input("\nAsk something (or type exit): ")

    if query.lower() == "exit":
        break

    answer = ask_ai(query)
    print("\nAI:", answer)