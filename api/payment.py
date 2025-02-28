import os
import requests

def verify_payment(reference):
    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("status") and data["data"]["status"] == "success":
        return True
    return False
