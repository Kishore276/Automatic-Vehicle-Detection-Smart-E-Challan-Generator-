import os
os.environ['KMP_DUPLICATE_LIB_OK']= 'TRUE'
import smtplib,ssl
#This email is for testing and it is fully used for educational purpose
sender_email = "g.yuvakishorereddy@gmail.com"
password = "nqym gmql yqxb mgvn"


receiver_email = "99220040268@klu.ac.in"

def mail(subject, text):


    message = f"""From: <{sender_email}>
To: <{receiver_email}>
Subject: {subject}


{text}
"""

    context = ssl.create_default_context()
    print("Sending mail to", receiver_email)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
#

#
# import os
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# # Set environment variable to avoid OpenMP duplicate library issue
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
#
# # Email credentials
# sender_email = "fakemailforprojects@gmail.com"  # Corrected email
# password = "99220040816@Ram"  # Use App Password if 2FA is enabled
# receiver_email = "g.yuvakishorereddy@gmail.com"
#
# def send_email(subject, text):
#     """
#     Sends an email using Gmail's SMTP server.
#
#     Args:
#         subject (str): The subject of the email.
#         text (str): The body of the email.
#     """
#     # Create the email message
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject
#
#     # Attach the email body
#     message.attach(MIMEText(text, "plain"))
#
#     try:
#         # Create a secure SSL context
#         context = ssl.create_default_context()
#
#         # Log in to the SMTP server and send the email
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.ehlo()  # Identify yourself to the server
#             server.starttls(context=context)  # Upgrade the connection to secure
#             server.ehlo()
#             server.login(sender_email, password)  # Log in to the server
#             server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
#
#         print(f"Email sent successfully to {receiver_email}.")
#     except smtplib.SMTPAuthenticationError:
#         print("Error: Authentication failed. Check your email and password.")
#     except smtplib.SMTPException as e:
#         print(f"Error: Unable to send email. {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#
# # Example usage
# subject = "Test Email"
# text = "This is a test email sent from Python."
# send_email(subject, text)

#
# import os
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# # Set environment variable to avoid OpenMP duplicate library issue
# os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
#
# # Email credentials (use environment variables for security)
# sender_email = os.getenv("SENDER_EMAIL", "g.yuvakishorereddy@gmail.com")  # Replace with your email
# password = os.getenv("EMAIL_PASSWORD", "nqym gmql yqxb mgvn")  # Use App Password if 2FA is enabled
# receiver_email = "99220040268@klu.ac.in"  # Replace with recipient email
#
# def send_email(subject, text):
#     """
#     Sends an email using Gmail's SMTP server.
#
#     Args:
#         subject (str): The subject of the email.
#         text (str): The body of the email.
#     """
#     # Create the email message
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject
#
#     # Attach the email body
#     message.attach(MIMEText(text, "plain"))
#
#     try:
#         # Create a secure SSL context
#         context = ssl.create_default_context()
#
#         # Log in to the SMTP server and send the email
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.ehlo()  # Identify yourself to the server
#             server.starttls(context=context)  # Upgrade the connection to secure
#             server.ehlo()
#             server.login(sender_email, password)  # Log in to the server
#             server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
#
#         print(f"Email sent successfully to {receiver_email}.")
#     except smtplib.SMTPAuthenticationError:
#         print("Error: Authentication failed. Check your email and password.")
#     except smtplib.SMTPException as e:
#         print(f"Error: Unable to send email. {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#
# # Example usage
# subject = "Test Email"
# text = "This is a test email sent from Python."
# send_email(subject, text)