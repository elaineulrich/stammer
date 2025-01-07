import requests

def create_hubspot_webhook():
    url = 'https://api.hubapi.com/webhooks/v3/subscriptions'
    headers = {
        'Authorization': f'Bearer {HUBSPOT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "subscriptionUrl": "https://your-server.com/webhook",  # Your endpoint to receive webhook events
        "events": [
            "conversations.message.sent"
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
