from flask import request, jsonify
import requests
import os
from app import app

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        webhook_data = request.json
        print(webhook_data)
        # Extract required data
        pr_number = webhook_data['number']
        comments_url = webhook_data['pull_request']['_links']['comments']['href']
        repo_url = webhook_data['pull_request']['head']['repo']['clone_url']
        branch_name = webhook_data['pull_request']['head']['ref']

        # Create a temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the repository
            repo = Repo.clone_from(repo_url, temp_dir)
            repo.git.checkout(branch_name)
            
            # Run pylint on the Python files
            pylint_output = ''
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            result = subprocess.run(
                                ['pylint', file_path],
                                capture_output=True,
                                text=True
                            )
                            if result.stdout:
                                pylint_output += f"File: {file}\n{result.stdout}\n\n"
                        except Exception as e:
                            pylint_output += f"Error analyzing {file}: {str(e)}\n"
            # GitHub API configuration
            headers = {
                'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}',
                'Accept': 'application/vnd.github.v3+json'
            }

        # GitHub API configuration
        headers = {
            'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}',
            'Accept': 'application/vnd.github.v3+json'
        }
        # Prepare comment with pylint results
        comment_data = {
            'body': f'Pylint Analysis Results:\n```\n{pylint_output or "No pylint errors found."}\n```'
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