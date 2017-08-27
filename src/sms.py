import nexmo
import json

url = "https://rest.nexmo.com/sms/json"
api_key = None
api_secret = None
sender = "Domain Notifier"

with open("../config.json") as config:
    configJson = json.load(config)
    api_key = configJson['api_key']
    api_secret = configJson['api_secret']


class SMS:

    def __init__(self, recipient):
        self.recipient = recipient
        self.client = nexmo.Client(key=api_key, secret=api_secret)
    
    def sendSms(self, body):
        self.client.send_message({
            'from':sender,
            'to': self.recipient,
            'text': body
        })

    def setRecipient(self, recipient):
        self.recipient = recipient
    
    def getRecipient(self, recipient):
        return self.recipient
