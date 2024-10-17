import requests
import json

# Your API key
API_KEY = your api key

# URL for the Gemini API
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

# Payload
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "What is coding?"
                }
            ]
        }
    ]
}

headers = {
    'Content-Type': 'application/json'
}

# Sending the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    data = response.json()
    
    # Extract and print the content before the breakdown
    content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No content found.")
    
    # Split the content based on "Here's a breakdown:"
    part_before_breakdown = content.split("Here's a breakdown:")[0]
    
    # Print the result
    print(part_before_breakdown)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}, Error: {response.text}")
