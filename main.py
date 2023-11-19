import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

#emails = ["25bauroth@da.org", "25ryan@da.org", "25", "25", "25kim@da.org", "25st", "25swigart@da.org", "25barrit@da.org", "26", "25", "25bhutani", "25moore@da.org", "25", "25windram@da.org", "25patkar@da.org", "25brady@da.org", "25", "25yoon@da.org", "25cook@da.org", "25mcnealy@da.org", "25pastor-valverde@da.org", "25chen@da.org", "25", "25", "25wang@da.org"]
names = ["Ryan Bauroth", "Kate Ryan", "Myles Z", "Marcus", "Justin Kim", "Jacob", "Preston Swigart", "Tyler Barrit", "Marco", "Angel", "Hardit", "Ori Moore", "Danielle Li", "Emerson Windram", "Aneesh Patkar", "Chris Brady", "Kyngston", "Joshua Yoon", "Angus Cook", "Nolan McNealy", "Luis Pastor-Valverede", "Lexie Chen", "Eva", "Naomi", "Nicholas Wang"]
names_copy = ["Ryan Bauroth", "Kate Ryan", "Myles Z", "Marcus", "Justin Kim", "Jacob", "Preston Swigart", "Tyler Barrit", "Marco", "Angel", "Hardit", "Ori Moore", "Danielle Li", "Emerson Windram", "Aneesh Patkar", "Chris Brady", "Kyngston", "Joshua Yoon", "Angus Cook", "Nolan McNealy", "Luis Pastor-Valverede", "Lexie Chen", "Eva", "Naomi", "Nicholas Wang"]
assigned = ["" for i in range(len(names))]
email = ["ryanbauroth6@gmail.com" for i in range(len(names))]

email_sender = "vibesecretsanta@gmail.com"
email_password = "EMAIL_KEY"
email_receiver = "ryanbauroth6@gmail.com"

subject = 'Your Secret Santa Assignee Is...'

em = MIMEMultipart("alternative")
em['From'] = email_sender

for n in range(len(names)):
    rand = random.randint(0, len(names_copy) - 1)
    while names[n] is names_copy[rand]:
        rand = random.randint(0, len(names_copy) - 1)
    assigned[n] = names_copy[rand]
    names_copy.pop(rand)

    em["To"] = email[n]
    em['Subject'] = subject

    # Create the plain-text and HTML version of your message
    text = """\
    Hello """ + names[n].split()[0] + """"!
    
    You are assigned """ + assigned[n] + """ for the DA Secret Santa! 
    
    Reminder that there is a spending limit of $20!
    
    In case of...
    - an assignee you REALLY don't think you can give a good gift to
    - something stopping you from delivering/getting a gift (including not wanting to participate)
    - etc
    ...reach out to Ryan!
    
    Thank you so much for participating and have fun!
    """
    html = """\
    <html>
      <body>
        <p>Hello """ + names[n].split()[0] + """!<br>
        <br>
            You are Assigned <strong>""" + assigned[n] + """</strong> for the DA Secret Santa!  
            <br> 
            <br>
            Reminder that there is a <strong>spending limit of $20!</strong>
            <br>
            <br>
            In case of...
        </p>
        <ul>
            <li>an assignee you REALLY don't think you can give a good gift to</li>
            <li>something stopping you from delivering/getting a gift (including not wanting to participate)</li>
            <li>etc</li>
        </ul>
        <p>
            ...reach out to Ryan!
            <br>
            <br>
            Thank you so much for participating and have fun!
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    em.attach(part1)
    em.attach(part2)

    context = ssl.create_default_context()

    #with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
     #   smtp.login(email_sender, email_password)
     #   smtp.sendmail(email_sender, email_receiver, em.as_string())

with open('assignees.txt', 'w') as fp:
    for a in range(len(assigned)):
        # write each item on a new line
        fp.write(names[a] + " => " + assigned[a] + "\n")