# login_helper.py
from kiteconnect import KiteConnect
import webbrowser
from data.kite_client import KiteClient

def login_and_inject():
    """Interactive login, returns kite object and injects into KiteClient."""
    print("\n" + "="*50)
    print(" KITE LOGIN")
    print("="*50)
    api_key = input("Enter API Key: ").strip()
    api_secret = input("Enter API Secret: ").strip()

    kite = KiteConnect(api_key=api_key)
    login_url = kite.login_url()
    print(f"\nOpen this URL in your browser:\n{login_url}")
    open_browser = input("Open browser automatically? (y/n): ").strip().lower()
    if open_browser == 'y':
        webbrowser.open(login_url)

    request_token = input("Enter the request_token from the URL: ").strip()

    try:
        session = kite.generate_session(request_token, api_secret=api_secret)
        access_token = session["access_token"]
        kite.set_access_token(access_token)
        print("✅ Login successful.\n")

        # Inject into KiteClient singleton
        kite_client = KiteClient()
        kite_client.set_kite_instance(kite)

        return kite
    except Exception as e:
        print(f"❌ Login failed: {e}")
        raise
