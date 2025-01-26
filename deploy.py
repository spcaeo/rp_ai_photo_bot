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
            subprocess.run(['git', 'add'] + files, check=True)
        if commit_message:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Git push successful")
        
        # Initial deployment
        url = f"https://api.render.com/v1/services/{service_id}/deploys"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(url, headers=headers)
        deploy_data = response.json()
        deploy_id = deploy_data['id']
        print(f"Deployment initiated: {deploy_id}")
        
        # Check deployment status
        status = "build_in_progress"
        while status in ["build_in_progress", "update_in_progress"]:
            time.sleep(10)
            status_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}"
            status_response = requests.get(status_url, headers=headers)
            status_data = status_response.json()
            status = status_data.get('status', 'unknown')
            if status == 'canceled':
                print("⚠️  Deployment was canceled")
                break
            elif status == 'failed':
                print("❌ Deployment failed")
                break
            elif status == 'live':
                print("✅ Deployment successful")
                break
            else:
                print(f"🔄 Current status: {status}")
        
        with open('notes.txt', 'a') as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"Commit: {deploy_data['commit']['id'][:7]}\n")
            f.write(f"Message: {commit_message}\n")
            f.write(f"Deploy ID: {deploy_id}\n")
            f.write(f"Final Status: {status}\n")
            if status != 'live':
                f.write("Error: Deployment did not complete successfully\n")
            f.write("-" * 50 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        with open('notes.txt', 'a') as f:
            f.write(f"\n[{timestamp}] ERROR: {str(e)}\n")
            f.write("-" * 50 + "\n")

if __name__ == "__main__":
    git_and_deploy(['.env', 'deploy.py', 'notes.txt'], "Added detailed status tracking and emojis")