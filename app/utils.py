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

    

        #var values = [604800, 1209600,1814400, /*weeks: 1 to 3*/
            #2419200,4838400,7257600,9676800,12096000,14515200,16934400,19353600,21772800,24192000,26611200, /*months: 1 to 11*/
            #29030400, 58060800, 87091200]; /*years: 1 to 3*/