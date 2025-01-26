import subprocess
import requests

def git_and_deploy(files=None, commit_message=None):
    # Git operations with error handling
    try:
        if files:
            subprocess.run(['git', 'add'] + files)
        else:
            subprocess.run(['git', 'add', '.'])
            
        if commit_message:
            subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])
    except Exception as e:
        print(f"Git error: {e}")

    # Render deployment
    service_id = "srv-cuasr5rtq21c73cfgm9g"
    api_key = "rnd_XcX9aEhsudw7SeUO8iTOckRLliPo"
    
    url = f"https://api.render.com/v1/services/{service_id}/deploys"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.post(url, headers=headers)
    print(f"Deployment Status: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    git_and_deploy(['.env', 'deploy.py', 'notes.txt'], "Adding new files")