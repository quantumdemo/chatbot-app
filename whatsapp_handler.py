import os
import json
import requests
from flask import Flask, request

def handle_whatsapp_message(request):
    """
    Handles incoming WhatsApp messages.
    """
    # Parse the incoming message
    message = request.get_json()
    if message.get('object') == 'whatsapp_business_account':
        for entry in message.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    for message_data in change.get('value', {}).get('messages', []):
                        if message_data.get('type') == 'text':
                            # Process the text message
                            process_text_message(message_data)
    return 'OK'

def handle_whatsapp_message(request):
    """
    Handles incoming WhatsApp messages.
    """
    # Parse the incoming message
    message = request.get_json()
    if message.get('object') == 'whatsapp_business_account':
        for entry in message.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    for message_data in change.get('value', {}).get('messages', []):
                        if message_data.get('type') == 'text':
                            # Process the text message
                            process_text_message(message_data)
                        elif message_data.get('type') == 'interactive':
                            process_interactive_message(message_data)
    return 'OK'

def process_text_message(message_data):
    """
    Processes a text message and sends a response.
    """
    phone_number = message_data.get('from')
    message_body = message_data.get('text', {}).get('body')

    # Here you would typically use your chatbot's logic to generate a response
    from app import chatbot_response
    response_body = chatbot_response(message_body, phone_number)

    # Send the response back to the user
    send_whatsapp_message(phone_number, response_body)

def process_interactive_message(message_data):
    """
    Processes an interactive message and sends a response.
    """
    phone_number = message_data.get('from')
    button_id = message_data.get('interactive', {}).get('button_reply', {}).get('id')

    # Here you would typically use your chatbot's logic to generate a response
    from app import chatbot_response
    response_body = chatbot_response(button_id, phone_number)

    # Send the response back to the user
    send_whatsapp_message(phone_number, response_body)

def send_whatsapp_message(to, text):
    """
    Sends a WhatsApp message.
    """
    send_whatsapp_message_with_buttons(to, text, [])

def send_whatsapp_message_with_buttons(to, text, buttons):
    """
    Sends a WhatsApp message with buttons.
    """
    url = f"https://graph.facebook.com/v13.0/{os.getenv('WHATSAPP_PHONE_NUMBER_ID')}/messages"
    headers = {
        "Authorization": f"Bearer {os.getenv('WHATSAPP_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
    }
    if buttons:
        data["type"] = "interactive"
        data["interactive"] = {
            "type": "button",
            "body": {
                "text": text
            },
            "action": {
                "buttons": buttons
            }
        }
    else:
        data["text"] = {
            "body": text
        }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
