from twilio.rest import Client
from flask import Flask, request
import json
import os

app = Flask(__name__)

account_sid = 'xxxXXxxXXXXx'
auth_token = 'YYyyYYyYYyYyY'
client = Client(account_sid, auth_token)

LOG_FILE = 'messages_log.json'

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
def save_logs(logs):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)



@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    response_msg = "Olá, sou um sistema de respostas automáticas. Como posso ajudar você hoje? \n Para saber nossos horários: 1 \n Para endereço digite: 2"
    print(f"Mensagem recebida de {from_number}: {incoming_msg}")

    if 'oi' in incoming_msg:
        response_msg = "Olá! Como posso ajudar você hoje?"
    elif '1' in incoming_msg:
        response_msg = "Nosso horário de atendimento é das 9h às 18h, de segunda a sexta-feira."
    elif '2' in incoming_msg:
        response_msg = "Estamos localizados na Rua 1,  Niteroi."

    message = client.messages.create(
        from_='whatsapp:+14155238886',  
        body=response_msg,
        to=from_number
    )

    logs = load_logs()
    logs.append({
        'from_number': from_number,
        'incoming_msg': incoming_msg,
        'response_msg': response_msg,
        'timestamp': message.date_created.isoformat()
    })
    save_logs(logs)

    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
