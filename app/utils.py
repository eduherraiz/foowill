 #-*- coding: UTF-8 -*-
def send_email_mandrill(subject, text_content, html_content, from_email, from_name, email_to, name_to):
    from mailsnake import MailSnake
    from django.conf import settings

    'Send email using mandrill.com API'
    mapi = MailSnake(settings.MANDRILL_KEY, api='mandrill')
    message={
        'subject':subject, 
        'text': text_content,
        'html': html_content,
        'from_email': from_email, 
        'from_name':from_name, 
        'to':[{
            'email':email_to, 
            'name': name_to,
        }]
    }
    return mapi.messages.send(message=message) 
