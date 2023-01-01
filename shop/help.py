# from email import message
from django.core.mail import send_mail
#import uuid
from django.conf import settings


def sendmail(email, fname):
    subject = f"welcome {fname}"
    message = f'{fname} you are at right place for sopping \n  confirm your account hai,'
    email_from = settings.EMAIL_HOST_USER
    send_to = [email]
    send_mail(subject, message, email_from, send_to)
    return True

# http://127.0.0.1:8000/reset/{token}

# def sendmail_resetpasswod(email,fname,token):
#     token = token 
#     subject = f"oe {fname} .Manxe tw hos nee tw muji kashari birshis tw muji password jasto chees nee"
#     message = f'''la randi ko aba yo link ma ja ani http://127.0.0.1:8000/reset/{token} \n feri nabirshi nee. 
#                 arko pali nee feri ais vane tera paile gad linxu ani matri password dinxu'''
#     email_from = settings.EMAIL_HOST_USER
#     send_to = [email]
#     send_mail(subject, message, email_from, send_to)
#     return True
def forgetpassword(emial, token):
    token = token
    subject = 'your forget password'
    message = f'click the below link to change the password  http://127.0.0.1:8000/change/{token}/'
    emial_from = settings.EMAIL_HOST_USER
    send_to = [emial]
    send_mail(subject, message, emial_from, send_to)
    return True