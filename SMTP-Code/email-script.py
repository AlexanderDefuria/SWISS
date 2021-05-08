import smtplib
from email.message import EmailMessage
# Create the message for the email
email_message = "Hello this is a message from a script"

# Create EmailMessage Object
email = EmailMessage()
# Who is the email from
email["from"] = "Alex"
# To which email you want to send the email
email["to"] = "recipent@email.com"
# Subject of the email
email["subject"] = "This is from a python script"
email.set_content(email_message)

# Create smtp server
with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    # Connect securely to server
    smtp.starttls()
    # Login using username and password to dummy email. Remember to set email to allow less secure apps if using Gmail
    smtp.login("email@gmail.com", "password")
    # Send email.
    smtp.send_message(email)
# To configure your gmail account to use less secure apps, first sign in then goto account settings, 
# then to security, then scroll down to 'Less secure apps' and click allow. Done!