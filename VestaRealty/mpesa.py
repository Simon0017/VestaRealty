import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from .validators import *

# func to get the access token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json().get("access_token")


# func to do the stk push
def stk_push(phone, amount, account_reference, callback_url,shortcode,transaction_type="CustomerPayBillOnline"):
    if not shortcode:
        return
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode()
    
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type,
        "Amount": validate_amount(amount),
        "PartyA": phone ,#validate_possible_number(phone,"Kenya").as_e164[1:],
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": validate_reference(account_reference),
        "TransactionDesc": "Payment to landlord"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# func to Implement C2B for Paybill or Till Number Payments
# NOT NECESSARY
def register_c2b_url():
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": "http://127.0.0.1:8000/confirmation/",
        "ValidationURL": "http://127.0.0.1:8000/validation/",
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
