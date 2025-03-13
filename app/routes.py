from flask import request, jsonify
import requests
import tempfile
import os
from git.repo.base import Repo
from app import app
import subprocess

#path in render /opt/render/project/src

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the event payload
    payload = request.json
    
    # Get routes.py file path
    routes_file = os.path.abspath(__file__)
    
    try:
        # Run pylint on routes.py
        result = subprocess.run(
            ['python', '-m', 'pylint', routes_file],
            capture_output=True,
            text=True
        )
        
        # GitHub API configuration
        headers = {
            'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Prepare comment with pylint results
        comment_data = {
            'body': f'Pylint Analysis Results for routes.py:\n```\n{result.stdout or "No pylint errors found."}\n```'
        }
        
        # Post comment to GitHub
        comments_url = payload['pull_request']['comments_url']
        response = requests.post(comments_url, headers=headers, json=comment_data)
        
        return jsonify({'status': 'success', 'message': 'Pylint analysis completed'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500