from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>L1_review this app will do a first level review of the pull request</h1>"

if __name__ == "__main__":
    app.run()