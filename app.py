from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>doing the l1 review</h1>"

@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        print(data)  # Print the raw JSON payload to the console
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failure'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)