import requests

HUBSPOT_API_KEY = 'b480fa1d-b381-4bad-9ae0-4e79d0bcf858'
INBOX_ID = '22375672'

def create_conversation_in_hubspot_inbox(conversation_data):
    url = f'https://api.hubapi.com/conversations/v3/inboxes/{INBOX_ID}/messages'
    headers = {
        'Authorization': f'Bearer {HUBSPOT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "message": {
            "body": conversation_data["message"],
            "sender": {
                "email": conversation_data["customer_email"]
            },
            "recipient": {
                "email": conversation_data["support_email"]
            }
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
