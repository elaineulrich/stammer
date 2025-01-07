import requests

def create_hubspot_webhook():
    url = 'https://api.hubapi.com/webhooks/v3/subscriptions'
    headers = {
        'Authorization': f'Bearer {HUBSPOT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "subscriptionUrl": "https://app.hubspot.com/oauth/authorize?client_id=1793bc7c-8fbf-40cf-b0a5-fc3db59d915f&redirect_uri=https://app.hubspot.com/oauth/authorize?client_id=1793bc7c-8fbf-40cf-b0a5-fc3db59d915f&scope=crm.schemas.quotes.read%20crm.schemas.contacts.write%20crm.objects.line_items.read%20crm.schemas.deals.read%20crm.objects.line_items.write%20crm.schemas.deals.write%20crm.objects.orders.write%20oauth%20crm.objects.orders.read%20crm.objects.courses.read%20conversations.read%20conversations.custom_channels.read%20crm.objects.courses.write%20conversations.write%20conversations.custom_channels.write%20crm.objects.leads.read%20conversations.visitor_identification.tokens.create%20crm.objects.leads.write%20crm.objects.users.read%20crm.objects.contacts.write%20crm.objects.users.write%20crm.objects.custom.read%20crm.objects.feedback_submissions.read%20crm.objects.custom.write%20crm.schemas.services.read%20crm.objects.companies.write%20crm.lists.write%20crm.objects.companies.read%20crm.schemas.listings.read%20crm.lists.read%20crm.objects.deals.read%20crm.schemas.listings.write%20crm.schemas.contacts.read%20crm.objects.deals.write%20crm.objects.quotes.write%20crm.objects.contacts.read%20crm.schemas.companies.read%20crm.objects.quotes.read",  # Your endpoint to receive webhook events
        "events": [
            "conversations.message.sent"
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
