import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_error_msg_via_email(port=587, smtp_server="smtp.gmail.com",
                             sender_email="ai.insights.au@gmail.com",
                             receiver_email="shane.zhong@gmail.com",
                             password="password",
                             subject="Notification - Twitter GPT-2 Model Failed",
                             error_msg="NA"):
    print("=" * 30)
    print("Sending email notification")
    print("=" * 30)

    print(smtp_server)
    print("Sender: " + sender_email)
    print("Receiver: " + receiver_email)
    print("PW: " + password[:1] + "*************************" + password[-1:])
    print(" ")
    print("Subject: " + subject)
    print("Error msg: " + error_msg)

    # Message Setting
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    message_template = """\
  This message is sent from Python Script.
  Below is the Twitter error message: 
  {msg}
  """
    text = message_template.format(msg=error_msg)
    print(text)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email,
                            receiver_email,
                            message.as_string())
            server.quit()
    except Exception as e:
        # Print any error messages to stdout
        print("=" * 30)
        print("ERROR MESSAGE:")
        print(e)
    else:
        print("=" * 30)
        print("Email Send!")

    return
