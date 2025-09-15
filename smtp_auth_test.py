import argparse
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host', required=True,
        type=str)
    parser.add_argument(
        '-P', '--port', required=False,
        type=int, default=25)
    parser.add_argument(
        '-u', '--username', required=True,
        type=str)
    parser.add_argument(
        '-p', '--password', required=True,
        type=str)
    parser.add_argument(
        '-r', '--recipient', required=False, type=str,
        help="Recipient email, defaults to the username if not provided")
    parser.add_argument(
        '-s', '--sender', required=False, type=str,
        help="Sender email, defaults to the username if not provided")
    parser.add_argument(
        '--no-login', required=False,
        action='store_true',
        help="Do not authenticate")
    parser.add_argument(
        '--no-tls', required=False,
        action='store_true',
        help="Do not use opportunistic TLS (STARTTLS)")
    parser.add_argument(
        '--smtps', required=False,
        action='store_true',
        help="Use SMTPS (implies --no-tls)")

    # If no arguments are provided, print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def send_email(host, port, username, password, sender, recipient, no_tls,
               no_login, use_smtps):
    if not sender:
        sender = username
    if not recipient:
        recipient = username

    subject = 'Test Email'
    body = 'Test body'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if use_smtps:
        smtp_cls = smtplib.SMTP_SSL
        no_tls = True
    else:
        smtp_cls = smtplib.SMTP

    try:
        with smtp_cls(host, port) as server:
            if not no_tls:
                server.starttls()
            if not no_login:
                server.login(username, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    args = parse_args()
    send_email(args.host, args.port, args.username, args.password, args.sender,
               args.recipient, args.no_tls, args.no_login, args.smtps)
