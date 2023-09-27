from django.contrib import messages
from django.core import mail
from django.conf import settings

from kavenegar import *
from config.settings import IN_DEVELOPMENT
import datetime
import time


api_key = '334F31594E50685144546739357A75617454396841706555536B394E425947436A7971514E546D495868413D'


def send_sms(request, phone_number, ver_code):
    WAITING_TIME = 60

    end = time.mktime(datetime.datetime.now().timetuple())
    start = request.session.get('start', (end - WAITING_TIME - 1))
    time_delta = end - start

    if time_delta > WAITING_TIME:
        try:
            api = KavenegarAPI(api_key)
            params = {
                'sender': '',
                'receptor': phone_number,
                'message': f'Your verification code is: "{ver_code}".',
            }
            if IN_DEVELOPMENT == True:
                messages.success(request, f'Message sent. "{ver_code}"')
            else:
                api.sms_send(params)
                messages.success(request, 'Message sent.')
            start = time.mktime(datetime.datetime.now().timetuple())
            request.session['start'] = start
        except APIException as e:
            messages.error(request, e)
        except HTTPException as e:
            messages.error(request, e)
    else:
        messages.info(
            request, f'You must wait "{int(WAITING_TIME - time_delta)}" seconds before retrying.')
        
        
def send_mail(user):
    subject = 'Welcome to Instagram!'
    message = f'Hi {user.username}, thank you for registering in Instagram.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    try:
        mail.send_mail(subject, message, email_from, recipient_list)
    except:
        pass
