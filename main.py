import requests

HUBSPOT_API_KEY = 'b480fa1d-b381-4bad-9ae0-4e79d0bcf858'

def create_or_update_contact(email, first_name, last_name, phone=None):
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    headers = {
        'Authorization': f'Bearer {HUBSPOT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Check if the contact already exists in HubSpot using email
    existing_contact = get_contact_by_email(email)
    if existing_contact:
        contact_id = existing_contact['id']
        return update_contact(contact_id, first_name, last_name, phone)
    else:
        return create_new_contact(email, first_name, last_name, phone)


def get_contact_by_email(email):
    url = f'https://api.hubapi.com/crm/v3/objects/contacts/search'
    params = {'q': email, 'properties': 'email'}
    response = requests.post(url, params=params, headers={'Authorization': f'Bearer {HUBSPOT_API_KEY}'})
    data = response.json()
    return data['results'][0] if data['results'] else None


def create_new_contact(email, first_name, last_name, phone=None):
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    data = {
        "properties": {
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
            "phone": phone
        }
    }
    response = requests.post(url, json=data, headers={'Authorization': f'Bearer {HUBSPOT_API_KEY}'})
    return response.json()


def update_contact(contact_id, first_name, last_name, phone=None):
    url = f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}'
    data = {
        "properties": {
            "firstname": first_name,
            "lastname": last_name,
            "phone": phone
        }
    }
    response = requests.patch(url, json=data, headers={'Authorization': f'Bearer {HUBSPOT_API_KEY}'})
    return response.json()
