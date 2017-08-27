# Domain-Expiry-Notifier-SMS
A server that checks every 5 seconds if a selected domain(s) has been renewed or expired and then sends an SMS message to the user as an alert

To install dependencies run:

```pip install requirements.txt```

Then add any number of domains you wish for the server to monitor in domains.txt
You will also need to create an account at nexmo for the api key and secret key which should be filled in the config.json

Then run with python:

```python main.py```

