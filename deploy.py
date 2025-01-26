import subprocess
import requests
import time
from datetime import datetime

def git_and_deploy(files=None, commit_message=None, max_retries=3):
    service_id = "srv-cuasr5rtq21c73cfgm9g"
    api_key = "rnd_XcX9aEhsudw7SeUO8iTOckRLliPo"
    
    try:
        # Git push
        if files:
            subprocess.run(['git', 'add'] + files, check=True)
        if commit_message:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("✅ Git push successful")
        
        retry_count = 0
        while retry_count < max_retries:
            # Deploy
            url = f"https://api.render.com/v1/services/{service_id}/deploys"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(url, headers=headers)
            deploy_data = response.json()
            deploy_id = deploy_data['id']
            
            # Monitor status with detailed logs
            status = "build_in_progress"
            while status in ["build_in_progress", "update_in_progress"]:
                time.sleep(10)
                status_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}"
                status_response = requests.get(status_url, headers=headers)
                status_data = status_response.json()
                
                # Get detailed status info
                build_logs_url = f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs"
                logs_response = requests.get(build_logs_url, headers=headers)
                
                status = status_data.get('status', 'unknown')
                print(f"\nStatus: {status}")
                print(f"Details: {status_data.get('status_info', '')}")
                if logs_response.status_code == 200:
                    print("Build logs:")
                    print(logs_response.json())
                
                if status == 'live':
                    print("✅ Deployment successful")
                    break
                elif status in ['canceled', 'failed']:
                    print(f"⚠️  Deployment {status}")
                    print(f"Reason: {status_data.get('status_info', 'Unknown')}")
                    retry_count += 1
                    break
            
            if status == 'live':
                break
            elif retry_count < max_retries:
                print(f"Retrying... ({retry_count + 1}/{max_retries})")
                time.sleep(5)
        
        # Log final status
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('notes.txt', 'a') as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"Status: {status}\n")
            f.write(f"Reason: {status_data.get('status_info', 'Unknown')}\n")
            if logs_response.status_code == 200:
                f.write("Build logs:\n")
                f.write(str(logs_response.json())[:500] + "...\n")
            f.write("-" * 50 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    git_and_deploy(['.env', 'deploy.py', 'notes.txt'], "Added detailed deployment logs and error tracking")