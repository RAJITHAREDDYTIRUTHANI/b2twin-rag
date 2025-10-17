import requests
import json
import time

# Wait a moment for the web app to start
time.sleep(2)

# Test the web app API
try:
    # Test the status endpoint
    response = requests.get("http://localhost:5000/api/status")
    print("Status endpoint response:")
    print(response.json())
    
    # Test asking a question
    question_data = {"question": "What is the temperature range?"}
    response = requests.post("http://localhost:5000/ask", 
                           headers={"Content-Type": "application/json"},
                           data=json.dumps(question_data))
    
    print("\nQuestion response:")
    print(response.json())
    
except requests.exceptions.ConnectionError:
    print("Web app is not running. Please start it with: python web_app.py")
except Exception as e:
    print(f"Error testing web app: {e}")
