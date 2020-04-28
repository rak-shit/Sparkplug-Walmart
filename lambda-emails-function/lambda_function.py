import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def lambda_handler(event, context):
    # send_mail(to_email, subject, html_content)
    """ 
    Sendgrid API module
    """
    message = Mail(
    from_email=os.environ.get('FROM_EMAIL'),
    to_emails=to_email,
    subject=subject,
    html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)