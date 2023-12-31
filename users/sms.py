import requests
import json
AUTH_TOKEN = #basic token
def sendsms(receiver_phone,message):
    url = 'https://api.orange.com/oauth/v3/token'
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    resp = requests.post(url, data=data, headers=headers)
    
    auth = resp.json()['token_type'] + " " + resp.json()['access_token']
    sender_phone = "2370000"
    url = f'https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{sender_phone}/requests'
    headers = {
        "Content-Type": "application/json",
        "Accept": 'application/json',
        "Authorization": auth
    }
    data = {
        "outboundSMSMessageRequest": {
            "address": "tel:+" + receiver_phone,
            "senderAddress": "tel:+" + sender_phone,
            "outboundSMSTextMessage": {
                "message": message
            }
        }
    }
    r = requests.post(url=url, data="", headers=headers)
    d = {
        "status": r.status_code,
        "content": r.json()
    }
    print(d)
    

if __name__ == "__main__":
    sendsms()
