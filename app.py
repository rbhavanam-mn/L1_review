from flask import Flask, request, jsonify

app = Flask(__name__)

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
        print(pr_data)
        #print(pr_data)  # Print the raw JSON payload to the console
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failure'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
