import subprocess
import requests
from datetime import datetime

def git_and_deploy(files=None, commit_message=None):
    # Add timestamp to notes.txt
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('notes.txt', 'a') as f:
        f.write(f"\n[{timestamp}] {commit_message}\n")
    
    try:
        if files:
            subprocess.run(['git', 'add'] + files)
        else:
            subprocess.run(['git', 'add', '.'])
            
        if commit_message:
            subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])

        service_id = "srv-cuasr5rtq21c73cfgm9g"
        api_key = "rnd_XcX9aEhsudw7SeUO8iTOckRLliPo"
        
        url = f"https://api.render.com/v1/services/{service_id}/deploys"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.post(url, headers=headers)
        print(f"Deployment Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    git_and_deploy(['.env', 'deploy.py', 'notes.txt'], "Updated deployment script with timestamps")