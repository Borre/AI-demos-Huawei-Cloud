import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DeepSeek API key
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

print("Testing DeepSeek API connection")
print(f"API Key exists: {bool(DEEPSEEK_API_KEY)}")

if DEEPSEEK_API_KEY:
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Say hello world"}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print("API connection successful!")
        print(f"Response: {result['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"API connection failed: {e}")
else:
    print("No API key found in environment variables")