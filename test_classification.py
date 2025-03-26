import requests
import json
import time
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_server(url, max_retries=5):
    """Wait for the server to become available."""
    for i in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            logger.info(f"Waiting for server to start (attempt {i+1}/{max_retries})...")
            time.sleep(2)
    return False

def test_classification():
    BASE_URL = "http://localhost:8000"
    
    # Start the FastAPI server (uncomment if needed)
    # server_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "src.main:app", "--reload"])
    
    try:
        # Wait for server to start
        if not wait_for_server(BASE_URL):
            logger.error("Server failed to start")
            return

        # 1. Upload classification rules
        with open('rules.json', 'rb') as f:
            rules_response = requests.post(
                f"{BASE_URL}/upload-rules",
                files={"file": ("rules.json", f, "application/json")}
            )
        logger.info(f"Rules upload response: {rules_response.json()}")

        # 2. Upload test email
        with open('test.eml', 'rb') as f:
            email_response = requests.post(
                f"{BASE_URL}/upload-email",
                files={"file": ("test.eml", f, "message/rfc822")}
            )
        
        # 3. Display results
        result = email_response.json()
        logger.info("\n=== Classification Results ===")
        logger.info(json.dumps(result, indent=2))

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    
    finally:
        # Uncomment if you started the server in this script
        # server_process.terminate()
        pass

if __name__ == "__main__":
    test_classification()
