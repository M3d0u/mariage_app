from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key

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
    statut_participation = request.form.get("statut_participation")  # Ensure it's not empty
    message = request.form.get("message")

    # Debugging: Print the received form data
    print("Received RSVP Data:")
    print(f"Name: {name}, Email: {email}, Status: {statut_participation}, Message: {message}")

    if not name or not email or not statut_participation or not message:
        return jsonify({"error": "All fields are required"}), 400

    data = {
        "email": email,
        "name": name,
        "particpe": statut_participation,
        "message": message
    }

    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 200:
        return jsonify({"success": "RSVP submitted successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send RSVP"}), 500


if __name__ == '__main__':
    app.run(debug=True)
