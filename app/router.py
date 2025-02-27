# app/routes.py
from flask import request, jsonify
from app import app

# Global variable to store PR data
pr_data = None

@app.route("/", methods=['GET'])
def home():
    global pr_data
    if pr_data:
        return f"<h1>PR Data: {pr_data}</h1>"
    else:
        return "<h1>No PR data available</h1>"

@app.route("/webhook", methods=['POST'])
def webhook():
    global pr_data
    if request.method == 'POST':
        pr_data = request.json
        print(pr_data)  # Print the raw JSON payload to the console
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failure'}), 400