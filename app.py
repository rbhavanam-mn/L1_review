from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>for the l1 review</h1>"

@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        if data and 'pull_request' in data:
            pr_info = data['pull_request']
            print(f"PR Title: {pr_info['title']}")
            print(f"PR URL: {pr_info['html_url']}")
            print(f"PR User: {pr_info['user']['login']}")
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failure'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)