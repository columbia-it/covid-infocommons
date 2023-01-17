from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
import imp
import os
import logging
from base64 import urlsafe_b64encode
from google.auth.credentials import Credentials
from googleapiclient.discovery import build
import smtplib

TRUE_VALUES = ['true', 't', '1', 'yes', 'y']
logger = logging.getLogger(__name__)

def check_enable_log():
    """
    Checks if logging is enabled
    """
    enable_log = os.getenv('SMTP_ENABLE_LOG', 'f')
    return enable_log.lower() in TRUE_VALUES

def check_enable_send():
    """
    Checks if sending email is enabled
    """
    disable_send = os.getenv('SMTP_DISABLE_SEND', 'f')
    return disable_send.lower() not in TRUE_VALUES

def check_use_gmail_api():
    """
    Checks if Gmail API can be used
    """
    use_gmail_api = os.getenv('SMTP_USE_GMAIL_API', 'f')
    return use_gmail_api.lower() in TRUE_VALUES

def check_use_ssl():
    """
    Checks if smtp uses SSL
    """
    use_ssl = os.getenv('SMTP_USE_SSL', 'f')
    return use_ssl.lower() in TRUE_VALUES

def _send_message_by_gmail_api(email_message):
    """
    Sends an email via Gmail API
    """
    msg_body = {'raw': urlsafe_b64encode(email_message.as_string().encode("utf-8")).decode("utf-8")}
    scopes = os.getenv('GMAIL_API_SCOPES', '').split(';')
    client_id = os.getenv('GMAIL_API_CLIENT_ID', '')
    client_secret = os.getenv('GMAIL_API_CLIENT_SECRET', '')
    refresh_token = os.getenv('GMAIL_API_REFRESH_TOKEN', '')
    token_uri = os.getenv('GMAIL_API_TOKEN_URI', 'https://oauth2.googleapis.com/token')
    service_name = os.getenv('GMAIL_API_SERVICE_NAME', 'gmail')
    api_version = os.getenv('GMAIL_API_VERSION', 'v1')
    user_id = os.getenv('GMAIL_API_USER_ID', 'me')
    creds = Credentials(None, client_id=client_id, client_secret=client_secret, refresh_token=refresh_token, token_uri=token_uri)
    send_error = None
    try:
        service = build(service_name, api_version, credentials=creds)
        message = (service.users().messages().send(userId=user_id, body=msg_body).execute())
        logger.debug('Gmail API Message: {}'.format(message))
    except Exception as err:
        send_error = '{}'.format(err)
        logger.error('Error on Gmail API: {}'.format(err))
    return send_error

def _send_message(email_message):
    """
    Sends an email via our own SMTP server
    """
    send_error = None
    try:
        smtp_host = os.getenv('SMTP_HOST', 'localhost')
        with smtplib.SMTP(smtp_host) as smtp:
            smtp.send_message(email_message)
    except smtplib.SMTPRecipientsRefused as err:
        send_error = "Recipients refused - {}".format(err)
        # log_send_error(send_error)
    except smtplib.SMTPResponseException as resp_error:
        send_error = "SMTP error[{}] - {}".format(resp_error.smtp_code, resp_error.smtp_error)
        # log_send_error(send_error)
    except smtplib.SMTPException as mail_error:
        send_error = "SMTP exception - {}".format(mail_error)
        # log_send_error(send_error)
    except OSError as os_error:
        send_error = "SMTP connection failed - {}".format(os_error)
        # log_send_error(send_error)
    return send_error

def send_email(from_address, to_addresses, cc_addresses, bcc_addresses, subject, body, attachments=None, reply_to=None):
    """
    Sends an email with the given information such as from address,
    the list of to addresses, the list of cc addresses, subject, and body
    """
    print('......4.....')
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)
    if cc_addresses:
        msg['Cc'] = ', '.join(cc_addresses)
    if bcc_addresses:
        msg['Bcc'] = ', '.join(bcc_addresses)
    if reply_to:
        msg['Reply-To'] = reply_to
    msg['Subject'] = '{}'.format(Header(subject, 'utf-8'))
    c_text = MIMEText('', 'html')
    enable_log = check_enable_log()
    print('......5.....')
    if enable_log:
        c_text.replace_header('content-transfer-encoding', 'quoted-printable')
    c_text.set_payload(body, 'utf-8')
    msg.attach(c_text)
    if attachments:
        for att in attachments:
            attach_msg = MIMEApplication(att.read())
            attach_msg.add_header(
                'content-disposition', 'attachment',
                filename=('utf-8', '', att.filename)
            )
            msg.attach(attach_msg)
    if enable_log:
        logger.debug('email: {}'.format(msg))
    has_error = None
    if check_enable_send():
        if check_use_gmail_api():
            has_error = _send_message_by_gmail_api(msg)
        elif check_use_ssl():
            has_error = _send_message_ssl(msg)
        else:
            has_error = _send_message(msg)
    if has_error:
        logger.debug('Error on sending email: {}'.format(has_error))
    return has_error