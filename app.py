from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load Webhook URL from environment variables
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_GOOGLE_MAPS = os.getenv("API_GOOGLE_MAPS")

@app.route('/')
def home():
    return render_template("index.html", API_GOOGLE_MAPS=API_GOOGLE_MAPS)

@app.route('/submit_rsvp', methods=['POST'])
def submit_rsvp():
    name = request.form.get("name")
    email = request.form.get("email")
    statut_participation = request.form.get("statut_participation")  
    brunch = request.form.get("statut_brunch") or 'pas invité'
    musique = request.form.get("musique") or 'pas invité'
    message = request.form.get("message")

    if not name or not email or not statut_participation:
        return jsonify({"error": "All fields are required"}), 400

    data = {
        "email": email,
        "name": name,
        "participe": statut_participation,
        "brunch": brunch,
        "musique": musique,
        "message": message
    }

    # Debugging: Print the received form data
    print("RSVP Data:")
    print(f"{data}")

    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 200:
        return jsonify({"success": "RSVP submitted successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send RSVP"}), 500


if __name__ == '__main__':
    app.run(debug=True)
