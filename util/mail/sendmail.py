# -*- coding:utf-8 -*-

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

import os


class SendMail:
    '''邮件发送'''

    def __init__(self):
        pass

    def send_mail(self, receiver, sender, sender_pwd, email_host, title, content, attachments=None):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = title
            msg['Form'] = sender
            msg['To'] = COMMASPACE.join(receiver)
            msg['Date'] = formatdate(localtime=True)
            msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(attachment, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
                msg.attach(part)

            smtp = smtplib.SMTP()
            smtp.connect(email_host)
            smtp.login(sender, sender_pwd)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            return True
        except Exception:
            raise

if __name__ == '__main__':
    print('sendMail')
