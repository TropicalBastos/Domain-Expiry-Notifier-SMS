import smtplib
from consoleColors import consoleColors
from email.mime.text import MIMEText

sender = "Domain Notifier"
recipient = "ian-bastos@live.com"

def sendEmail(body):

    msg = MIMEText(body)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = body
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    try:
        s.sendmail(sender, [recipient], msg.as_string())
    except Exception as e:
        print(consoleColors.FAIL + "Error in sending mail " + e.__str__() + consoleColors.ENDC)
    s.quit()