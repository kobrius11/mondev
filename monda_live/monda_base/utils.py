from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re

def textify(html):
    # Remove html tags and continuous whitespaces 
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()

def send_template_mail(recipients, subject, template, context):
    html_message = render_to_string(template, context)
    message = textify(html_message)
    try:
        sent = send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients, 
            subject=subject, 
            message=message, 
            html_message=html_message,
            fail_silently=False
        )
    except Exception as e:
        print(e.__class__.__name__, e)
    else:
        return sent
