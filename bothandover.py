def stop_stammer_ai_bot(conversation_id):
    url = f'https://api.stammer.ai/v1/conversations/{conversation_id}/stop'
    response = requests.post(url)
    return response.json()
