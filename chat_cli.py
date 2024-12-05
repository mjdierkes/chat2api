import json
import sys
import requests
from sseclient import SSEClient

def load_auth_token():
    """Load authentication token from auth.json"""
    try:
        with open('auth.json', 'r') as f:
            auth_data = json.load(f)
            return auth_data.get('accessToken')
    except FileNotFoundError:
        print("Error: auth.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in auth.json")
        sys.exit(1)

def chat_completion(message, model="gpt-4o"):
    """Make a streaming chat completion request"""
    token = load_auth_token()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Accept': 'text/event-stream'
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "stream": True
    }

    try:
        response = requests.post(
            'http://127.0.0.1:5005/v1/chat/completions',
            headers=headers,
            json=data,
            stream=True
        )
        
        response.raise_for_status()
        
        # Read the streaming response line by line
        for line in response.iter_lines():
            if line:
                # Remove "data: " prefix and decode
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Skip "data: " prefix
                        if data['choices'][0].get('delta', {}).get('content'):
                            print(data['choices'][0]['delta']['content'], end='', flush=True)
                    except json.JSONDecodeError:
                        continue
                    except KeyError:
                        continue

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return
    
    print()  # New line after completion

def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_cli.py 'Your message here'")
        sys.exit(1)
        
    message = ' '.join(sys.argv[1:])
    chat_completion(message)

if __name__ == "__main__":
    main()