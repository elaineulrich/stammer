import requests
import json

# HubSpot API credentials
hubspot_api_key = 'b480fa1d-b381-4bad-9ae0-4e79d0bcf858'
hubspot_contact_endpoint = f'https://api.hubapi.com/contacts/v1/contact/createOrUpdate/email/{{email}}?hapikey={hubspot_api_key}'

# Stammer.ai API credentials
stammer_api_key = 'c8fdf3685a7dfd9f17318426b16c306b13d67dd2'
stammer_endpoint = 'https://ai.corlandpartners.com/en/chatbot/api/v1/message/'  # Replace with actual endpoint

# Headers for API requests
hubspot_headers = {
    'Content-Type': 'application/json'
}


def handler(request):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Vercel!"}),
    }


# Get Stammer.ai conversation data
def get_stammer_conversation():
    response = requests.get(stammer_endpoint, headers={'Authorization': f'Bearer {stammer_api_key}'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching Stammer.ai data: {response.status_code}")
        return None

# Create or update HubSpot contact based on Stammer.ai conversation
def create_or_update_contact(contact_data):
    email = contact_data['email']
    contact_payload = {
        "properties": [
            {"property": "email", "value": email},
            {"property": "firstname", "value": contact_data['first_name']},
            {"property": "lastname", "value": contact_data['last_name']},
            {"property": "phone", "value": contact_data['phone']},
            # Add more properties as needed
        ]
    }

    # Make the request to HubSpot API to create or update the contact
    response = requests.post(hubspot_contact_endpoint.format(email=email), headers=hubspot_headers, json=contact_payload)
    
    if response.status_code == 200:
        print("Contact successfully created or updated in HubSpot")
    else:
        print(f"Error with HubSpot API: {response.status_code}")

# Main function to handle integration
def integrate_stammer_with_hubspot():
    conversation_history = get_stammer_conversation()
    
    if conversation_history:
        contact_data = {
            'email': conversation_history.get('email'),
            'full_name': conversation_history.get('full_name'),
            'contact_number': conversation_history.get('contact_number')
        }
        
        create_or_update_contact(contact_data)

# Run the integration
integrate_stammer_with_hubspot()


# HubSpot Engagements API endpoint for conversations
hubspot_engagements_endpoint = 'https://api.hubapi.com/engagements/v1/engagements'

# Capture Stammer.ai conversation as a HubSpot inbox conversation
def capture_conversation_in_hubspot(conversation_history):
    conversation_payload = {
        "engagement": {
            "type": "CONVERSATION",  # Change to 'TASK', 'EMAIL' or 'CALL' as needed
            "timestamp": conversation_history['timestamp'],
        },
        "associations": {
            "contactIds": [conversation_history['contact_id']],  # Use the actual contact ID
            "companyIds": [sconversation_history['company_id']],  # Optional
        },
        "metadata": {
            "body": conversation_history['conversation_text'],
            "subject": "Stammer.ai Conversation",
        }
    }

    response = requests.post(hubspot_engagements_endpoint, headers=hubspot_headers, json=conversation_payload)

    if response.status_code == 200:
        print("Conversation successfully captured in HubSpot Inbox")
    else:
        print(f"Error with HubSpot Inbox API: {response.status_code}")

# Example: Call this inside your main loop after getting Stammer data
capture_conversation_in_hubspot(conversation_history)


# Function to send a message from HubSpot to Stammer.ai
def send_message_to_stammer(contact_id, message):
    stammer_payload = {
        "contact_id": contact_id,
        "message": message,
        "timestamp": int(time.time() * 1000)
    }
    response = requests.post('https://api.stammer.ai/respond', headers={'Authorization': f'Bearer {stammer_api_key}'}, json=stammer_payload)
    if response.status_code == 200:
        print("Message sent to Stammer.ai")
    else:
        print(f"Error sending message to Stammer.ai: {response.status_code}")

# Function to send Stammer.ai response back to HubSpot Inbox
def send_stammer_response_to_hubspot(contact_id, message):
    hubspot_payload = {
        "engagement": {
            "type": "NOTE",  # Or use other types as required
            "timestamp": int(time.time() * 1000),
        },
        "associations": {
            "contactIds": [contact_id],
        },
        "metadata": {
            "body": message,
            "subject": "Stammer.ai Response"
        }
    }
    response = requests.post(hubspot_engagements_endpoint, headers=hubspot_headers, json=hubspot_payload)
    if response.status_code == 200:
        print("Stammer.ai response captured in HubSpot Inbox")
    else:
        print(f"Error with HubSpot Inbox API: {response.status_code}")

# Handling the two-way flow
def handle_two_way_communication(contact_id, message_from_hubspot):
    # Send HubSpot message to Stammer.ai
    send_message_to_stammer(contact_id, message_from_hubspot)

    # Simulate receiving a response from Stammer.ai
    stammer_response = "This is the bot response from Stammer.ai"
    
    # Send Stammer.ai response back to HubSpot
    send_stammer_response_to_hubspot(contact_id, stammer_response)


# Function to detect manual human response from HubSpot
def is_human_message(message):
    # This could be determined based on message metadata or API endpoint specifics
    return "manual" in message  # For example, if the message comes with a specific flag

# Hand-off to human if message is human-driven
def handoff_to_human(contact_id, message_from_hubspot):
    if is_human_message(message_from_hubspot):
        # Stop Stammer.ai bot automation
        stop_stammer_ai_automation(contact_id)
        print("Handoff to human detected. Stopping Stammer.ai bot automation.")

# Example function to stop Stammer.ai automation
def stop_stammer_ai_automation(contact_id):
    response = requests.post('https://api.stammer.ai/stop', headers={'Authorization': f'Bearer {stammer_api_key}'}, json={"contact_id": contact_id})
    if response.status_code == 200:
        print("Automation stopped in Stammer.ai.")
    else:
        print(f"Error stopping Stammer.ai automation: {response.status_code}")
