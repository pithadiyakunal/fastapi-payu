from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import requests

from urllib.parse import parse_qs
app = FastAPI()

# PayU merchant credentials
merchant_key = "62Boh5H7"
salt = "3qdfCkKgi1"
base_url = "https://sandboxsecure.payu.in/_payment"


class PaymentRequest(BaseModel):
    amount: float
    order_id: str
    email: str


# Endpoint to initiate a PayU payment
@app.post("/initiate-payment")
async def initiate_payment(payment_request: PaymentRequest):
    try:
        # Convert the amount to a string
        amount_str = str(payment_request.amount)

        # Calculate hash to secure the payment request
        hash_string = f"{merchant_key}|{payment_request.order_id}|{amount_str}|{payment_request.email}||||||||||{salt}"
        hash_encoded = hashlib.sha512(hash_string.encode()).hexdigest()

        # Prepare the form data for the payment request
        form_data = {
            "key": merchant_key,
            "txnid": payment_request.order_id,
            "amount": amount_str,
            "productinfo": "YOUR_PRODUCT_INFO",  # Replace with actual product info
            "firstname": "YOUR_CUSTOMER_NAME",  # Replace with customer's first name
            "email": payment_request.email,
            "phone": "YOUR_CUSTOMER_PHONE",  # Replace with customer's phone number
            "surl": "YOUR_SUCCESS_URL",  # Replace with your actual success URL
            "furl": "YOUR_FAILURE_URL",  # Replace with your actual failure URL
            "hash": hash_encoded,
            "service_provider": "payu_paisa",
        }

        # Redirect the user to PayU for payment
        redirect_url = f"{base_url}?{('&'.join([f'{key}={value}' for key, value in form_data.items()]))}"
        return {"redirect_url": redirect_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
