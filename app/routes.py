from flask import render_template, request, jsonify
from app import app

pr_data = None

@app.route('/')
def index():
    return render_template('index.html', pr_data=pr_data)

@app.route('/webhook', methods=['POST'])
def webhook():
    global pr_data
    pr_data = request.json
    return jsonify({"status": "success"})