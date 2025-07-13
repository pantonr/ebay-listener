from flask import Flask, request, jsonify, abort, redirect
from urllib.parse import urlencode
import hashlib

app = Flask(__name__)

VERIFICATION_TOKEN = "PantonrUltraSecureWebhookToken2025XYZabc123"
ENDPOINT_URL = "https://pantonr-ebay-listener-c53662eef1b0.herokuapp.com/ebay-account-deletion"

# Your eBay App credentials
EBAY_APP_ID = "PhilipAn-NewListi-PRD-9ce04b995-3898eb8f"  # Your production App ID
REDIRECT_URI = "https://pantonr-ebay-listener-c53662eef1b0.herokuapp.com/oauth-return"

@app.route("/")
def home():
    return """
    <h1>eBay OAuth Handler</h1>
    <p><a href="/start-oauth" style="background: #0064d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🔑 Authorize with eBay</a></p>
    <p><a href="/ebay-account-deletion">Account Deletion Endpoint</a></p>
    """

@app.route("/start-oauth")
def start_oauth():
    """Generate eBay OAuth URL with all required scopes"""
    scopes = [
        'https://api.ebay.com/oauth/api_scope/sell.inventory.readonly',
        'https://api.ebay.com/oauth/api_scope/sell.inventory',
        'https://api.ebay.com/oauth/api_scope/sell.account.readonly',
        'https://api.ebay.com/oauth/api_scope/sell.account',
        'https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly',
        'https://api.ebay.com/oauth/api_scope/sell.fulfillment',
        'https://api.ebay.com/oauth/api_scope/sell.marketing.readonly',
        'https://api.ebay.com/oauth/api_scope/sell.marketing',
        'https://api.ebay.com/oauth/api_scope/sell.finances',
        'https://api.ebay.com/oauth/api_scope/commerce.identity.readonly'
    ]
    
    params = {
        'client_id': EBAY_APP_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(scopes),
        'state': 'your-custom-state-value'  # Optional: for security
    }
    
    auth_url = f"https://auth.ebay.com/oauth2/authorize?{urlencode(params)}"
    return redirect(auth_url)

@app.route("/oauth-return", methods=["GET"])
def oauth_return():
    """Handle OAuth callback from eBay"""
    auth_code = request.args.get("code")
    error = request.args.get("error")
    error_description = request.args.get("error_description")
    expires_in = request.args.get("expires_in")
    state = request.args.get("state")

    if error:
        return f"""
        <h1>❌ OAuth Error</h1>
        <p><b>Error:</b> {error}</p>
        <p><b>Description:</b> {error_description}</p>
        <p><a href="/start-oauth">Try Again</a></p>
        """, 400

    if not auth_code:
        return """
        <h1>❌ No Authorization Code</h1>
        <p>No authorization code received from eBay.</p>
        <p><a href="/start-oauth">Try Again</a></p>
        """, 400

    return f"""
    <h1>✅ eBay OAuth Complete!</h1>
    <div style="background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px;">
        <p><b>Authorization Code:</b></p>
        <p style="font-family: monospace; word-break: break-all; background: white; padding: 10px; border: 1px solid #ddd;">{auth_code}</p>
    </div>
    <p><b>Expires In:</b> {expires_in} seconds</p>
    <p><b>State:</b> {state}</p>
    
    <h2>🔥 Next Steps:</h2>
    <ol>
        <li>Copy the authorization code above</li>
        <li>Use it in your Python script to exchange for an access token</li>
        <li>Start making API calls to list items on eBay</li>
    </ol>
    
    <h3>💡 Quick Exchange Code:</h3>
    <pre style="background: #f8f8f8; padding: 10px; border: 1px solid #ddd; overflow-x: auto;">
import requests
import base64

# Your credentials
app_id = "PhilipAn-NewListi-PRD-9ce04b995-3898eb8f"
cert_id = "PRD-ce04b9953e43-3302-4e36-9e79-9c0b"
auth_code = "{auth_code}"
redirect_uri = "https://pantonr-ebay-listener-c53662eef1b0.herokuapp.com/oauth-return"

# Exchange for access token
url = "https://api.ebay.com/identity/v1/oauth2/token"
credentials = f"{{app_id}}:{{cert_id}}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {{
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {{encoded_credentials}}'
}}

data = {{
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri
}}

response = requests.post(url, headers=headers, data=data)
print(response.json())
    </pre>
    
    <p><a href="/start-oauth">🔄 Get New Token</a></p>
    """

@app.route("/ebay-account-deletion", methods=["GET", "POST"])
def account_deletion():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            abort(400)
        to_hash = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        response_hash = hashlib.sha256(to_hash.encode("utf-8")).hexdigest()
        return jsonify({"challengeResponse": response_hash}), 200

    elif request.method == "POST":
        print("✅ Received deletion event:", request.json)
        return "", 200

if __name__ == "__main__":
    app.run()
