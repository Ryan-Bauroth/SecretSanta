import os
import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import pandas as pd
from os.path import join, dirname
from dotenv import load_dotenv

# env stuff
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# loads participant data
# should have 'names', 'emails', and potentially 'target' values
data = pd.read_csv('participants.csv')

# gets enviroment variables
EMAIL_KEY = os.environ.get("EMAIL_KEY")
SENDING_EMAIL_ADDRESS = os.environ.get("SENDING_EMAIL_ADDRESS")

# For Randomly Shuffling List (allows n+1 implementation)

# combined = list(zip(data["Names"], data["Emails"]))
# random.shuffle(combined)
# shuffled_names, shuffled_emails = zip(*combined)
#
# # Convert them back to lists (zip returns tuples)
# shuffled_names = list(shuffled_names)
# shuffled_emails = list(shuffled_emails)
#
# data = {"Names": shuffled_names, "Emails": shuffled_emails}

# sets the subject of the email
SUBJECT = 'SENIOR TAG TEST'
assigned = []

# sends one email for each user in the data arr (names col)
for n in range(len(data["Names"])):
    # gets random send time in order to avoid spam blocking
    random_float = random.uniform(1.0, 3.0)
    time.sleep(random_float)

    # Random Shuffle n+1 implementation
    if n == len(data["Names"]) - 1:
        assigned.append(data["Names"][0])
    else:
        assigned.append(data["Names"][n + 1])

    # alternative email (not HTML)
    em = MIMEMultipart("alternative")

    # from, to, and subject variables for the email
    em['From'] = SENDING_EMAIL_ADDRESS
    em["To"] = data["Emails"][n]
    em['Subject'] = SUBJECT

    # alternative message
    text = """\
        Hello """ + data["Names"][n].split()[0] + """"!
    
        You are assigned """ + assigned[n] + """ for the Secret Santa! 
        """
    with open('senior_tag.html', 'r') as f:
        html = f.read()

    # replace parts of the HTML with the name of the recipient and the name of the assignment
    html = html.replace("SUBJECT-FIRSTNAME", data["Names"][n].split()[0])
    html = html.replace("ASSIGNED-FULLNAME", assigned[n])

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # ie, if HTML is valid, it will be rendered instead of the alternative message
    em.attach(part1)
    em.attach(part2)

    context = ssl.create_default_context()

    # sends emails
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
       smtp.login(SENDING_EMAIL_ADDRESS, EMAIL_KEY)
       smtp.sendmail(SENDING_EMAIL_ADDRESS, data["Emails"][n], em.as_string())

with open('assignees.txt', 'w') as fp:
    for a in range(len(assigned)):
        # stars out the first user
        # (helpful if you don't want to leak who is assigned to someone when accessing the txt file)
        # if assigned[a] is data["Names"][0]:
        #     fp.write("*** => " + assigned[a] + "\n")
        # else:
        fp.write(data["Names"][a] + " => " + assigned[a] + "\n")