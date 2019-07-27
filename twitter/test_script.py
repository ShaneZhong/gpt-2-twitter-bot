import os
from fn_SendEmail import send_error_msg_via_email

# Email Checking Function
# Google G-mail blocks the email sending function when you use this for the first time in a new environment.
# Enable here: https://accounts.google.com/b/0/DisplayUnlockCaptcha
# If error, https://support.google.com/mail/answer/7126229?visit_id=636997950280030700-282303594&rd=2#cantsignin
print("=" * 30)
print("Call email function")
send_error_msg_via_email(error_msg="Testing Script", password=os.environ['email_password'])

print("="*30)
print("TEST COMPLETE! " * 3)
