from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store the latest PR details
latest_pr = {}

@app.route("/webhook", methods=['POST'])
def github_webhook():
    global latest_pr
    if request.method == 'POST':
        payload = request.json
        if 'pull_request' in payload:
            pr = payload['pull_request']
            latest_pr = {
                'title': pr['title'],
                'body': pr['body'],
                'url': pr['html_url']
            }
        return jsonify({'status': 'success'}), 200

@app.route("/", methods=['GET'])
def home():
    return render_template_string("""
        <h1>L1_review - First Level Review of Pull Requests</h1>
        {% if latest_pr %}
            <h2>Latest Pull Request</h2>
            <p><strong>Title:</strong> {{ latest_pr.title }}</p>
            <p><strong>Body:</strong> {{ latest_pr.body }}</p>
            <p><strong>URL:</strong> <a href="{{ latest_pr.url }}">{{ latest_pr.url }}</a></p>
        {% else %}
            <p>No pull request data available.</p>
        {% endif %}
    """, latest_pr=latest_pr)

if __name__ == "__main__":
    app.run(port=5000)