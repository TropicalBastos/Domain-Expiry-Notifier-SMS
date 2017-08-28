# Domain-Expiry-Notifier-SMS
A process that checks every 5 seconds if a selected domain(s) has been renewed or expired and then sends an SMS message to the user as an alert

To install dependencies run:

```pip install --upgrade -r requirements.txt```

Then add any number of domains you wish for the script to monitor in config.json, under domains
You will also need to create an account with nexmo for the api key and secret key which should be filled in the config.json
One last thing, you will need to add a receiving phone number in config.json so you can receive the texts

To run:

```./domainnotifier.sh```

To run in the background:

```./domainnotifier.sh --background```

For windows users you can run with python:

```python main.py```

##Changelog

Version 0.2
<ul>
    <li>Combined domains.txt with config.json so that two things are in one place</li>
    <li>Fixed major bug that threw an error if a domain was deleted from the config.json</li>    
</ul>

Version 0.1
<ul>
    <li>Initial version</li>
<ul>

