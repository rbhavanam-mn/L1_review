from flask import request, jsonify
import requests
import os

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        webhook_data = request.json
        
        # Extract required data
        pr_number = webhook_data['number']
        comments_url = webhook_data['pull_request']['_links']['comments']['href']
        
        # GitHub API configuration
        headers = {
            'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Prepare comment
        comment_data = {
            'body': 'need manager approval'
        }
        
        # Post comment
        response = requests.post(comments_url, headers=headers, json=comment_data)
        
        if response.status_code == 201:
            return jsonify({
                "status": "success",
                "message": f"Comment added to PR #{pr_number}"
            })
        
        return jsonify({
            "status": "error",
            "message": f"Failed to add comment. Status: {response.status_code}"
        }), 500
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500