import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
email_password = os.environ.get("EMAIL_KEY")

data = pd.read_csv('participants.csv')
assigned = []

email_sender = "vibesecretsanta@gmail.com"
subject = 'Your Secret Santa Assignee Is...'

for n in range(len(data["Names"])):
    rand = random.randint(0, len(data["Names"]) - 1)
    while n == rand or data["Names"][rand] in assigned:
        rand = random.randint(0, len(data["Names"]) - 1)
    assigned.append(data["Names"][rand])

    em = MIMEMultipart("alternative")
    em['From'] = email_sender
    em["To"] = data["Emails"][n]
    em['Subject'] = subject

    # Create the plain-text and HTML version of your message
    text = """\
        Hello """ + data["Names"][n].split()[0] + """"!
    
        You are assigned """ + assigned[n] + """ for the Secret Santa! 
        """
    with open('message.html', 'r') as f:
        html = f.read()

    html = html.replace("SUBJECT-FIRSTNAME", data["Names"][n].split()[0])
    html = html.replace("ASSIGNED-FULLNAME", assigned[n])

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    em.attach(part1)
    em.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
       smtp.login(email_sender, email_password)
       smtp.sendmail(email_sender, data["Emails"][n] , em.as_string())

with open('assignees.txt', 'w') as fp:
    for a in range(len(assigned)):
        # write each item on a new line
        if assigned[a] is data["Names"][0]:
            fp.write("*** => " + assigned[a] + "\n")
        else:
            fp.write(data["Names"][a] + " => " + assigned[a] + "\n")