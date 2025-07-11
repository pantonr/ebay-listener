from flask import Flask, request, abort

app = Flask(__name__)

VERIFICATION_TOKEN = "PantonrUltraSecureWebhookToken2025XYZabc123"

@app.route("/ebay-account-deletion", methods=["POST"])
def account_deletion():
    token = request.headers.get("X-Verification-Token")
    if token != VERIFICATION_TOKEN:
        abort(403)
    print("Received deletion event:", request.json)
    return "", 200

if __name__ == "__main__":
    app.run()
