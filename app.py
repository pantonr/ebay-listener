from flask import Flask, request, jsonify, abort
import hashlib

app = Flask(__name__)

VERIFICATION_TOKEN = "PantonrUltraSecureWebhookToken2025XYZabc123"
ENDPOINT_URL = "https://pantonr-ebay-listener-c53662eef1b0.herokuapp.com/ebay-account-deletion"

@app.route("/ebay-account-deletion", methods=["GET", "POST"])
def account_deletion():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            abort(400)
        to_hash = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        response_hash = hashlib.sha256(to_hash.encode('utf-8')).hexdigest()
        return jsonify({"challengeResponse": response_hash}), 200

    elif request.method == "POST":
        # ✅ For testing: accept all POSTs and log them.
        print("Received deletion event:", request.json)
        return "", 200

if __name__ == "__main__":
    app.run()
