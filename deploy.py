import subprocess
import requests
import time
from datetime import datetime

def git_and_deploy(files=None, commit_message=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    service_id = "srv-cuasr5rtq21c73cfgm9g"
    api_key = "rnd_XcX9aEhsudw7SeUO8iTOckRLliPo"
    
    try:
        # Git operations
        if files:
            subprocess.run(['git', 'add'] + files)
        if commit_message:
            subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])
        
        # Initial deployment
        url = f"https://api.render.com/v1/services/{service_id}/deploys"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(url, headers=headers)
        deploy_data = response.json()
        deploy_id = deploy_data['id']
        
        # Check deployment status until complete
        status = "build_in_progress"
        while status in ["build_in_progress", "update_in_progress"]:
            time.sleep(10)  # Wait 10 seconds between checks
            status_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}"
            status_response = requests.get(status_url, headers=headers)
            status_data = status_response.json()
            status = status_data.get('status', 'unknown')
            print(f"Current status: {status}")
        
        # Log final status
        with open('notes.txt', 'a') as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"Commit: {deploy_data['commit']['id'][:7]}\n")
            f.write(f"Message: {commit_message}\n")
            f.write(f"Deploy ID: {deploy_id}\n")
            f.write(f"Final Status: {status}\n")
            f.write("-" * 50 + "\n")
        
        print(f"Final Deployment Status: {status}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    git_and_deploy(['.env', 'deploy.py', 'notes.txt'], "Added final deployment status check")