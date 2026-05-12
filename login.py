from kiteconnect import KiteConnect
import webbrowser
import os
import json

def login():
    api_key = input("Enter your Kite API Key: ").strip()
    api_secret = input("Enter your Kite API Secret: ").strip()
    
    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()
    print(f"Open this URL in your browser: {login_url}")
    webbrowser.open(login_url)  # optional
    request_token = input("Enter the request token from the URL after login: ").strip()
    
    try:
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        # Save token to file
        with open("access_token.txt", "w") as f:
            f.write(access_token)
        # Also save api_key for later? We'll store separately
        with open("api_key.txt", "w") as f:
            f.write(api_key)
        print("Login successful. Access token saved.")
        return access_token
    except Exception as e:
        print(f"Login failed: {e}")
        return None

if __name__ == "__main__":
    login()
