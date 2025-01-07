from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_hubspot_webhook():
    data = request.json
    # Parse the incoming data
    message = data['object']['message']['body']
    customer_email = data['object']['sender']['email']
    
    # Send the message data to Stammer.ai to update conversation history
    update_conversation_in_stammer_ai(customer_email, message)
    
    return jsonify({"status": "success"}), 200

def update_conversation_in_stammer_ai(email, message):
    # Assuming you have Stammer.ai API to update conversations
    url = 'https://ai.corlandpartners.com/en/chatbot/api/v1/message/'
    data = {
        "email": email,
        "message": message
    }
    response = requests.post(url, json=data)
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
