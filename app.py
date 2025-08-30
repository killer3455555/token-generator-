from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

# Apna APP_ID aur APP_SECRET dalna (jo FB Developers se milega)
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
REDIRECT_URI = "http://localhost:5000/callback"

@app.route("/")
def home():
    fb_auth_url = (
        "https://www.facebook.com/v15.0/dialog/oauth?"
        f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope=pages_messaging,groups_access_member_info"
    )
    return f'<a href="{fb_auth_url}">Login with Facebook</a>'

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code returned"

    # Step 1: Get Short-Lived Token
    token_url = (
        f"https://graph.facebook.com/v15.0/oauth/access_token?"
        f"client_id={APP_ID}&redirect_uri={REDIRECT_URI}&client_secret={APP_SECRET}&code={code}"
    )
    token_res = requests.get(token_url).json()
    short_lived_token = token_res.get("access_token")

    # Step 2: Convert to Long-Lived Token
    exchange_url = (
        f"https://graph.facebook.com/v15.0/oauth/access_token?"
        f"grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={short_lived_token}"
    )
    exchange_res = requests.get(exchange_url).json()
    long_lived_token = exchange_res.get("access_token")

    return f"✅ Your Long-Lived Token:<br><textarea rows='5' cols='60'>{long_lived_token}</textarea>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
