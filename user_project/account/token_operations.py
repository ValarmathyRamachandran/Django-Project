import base64
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import request
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.baseconv import base64
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from jwt import decode

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.http import HttpResponse

from django.core.mail import send_mail


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


class Common:
    # @staticmethod
    # def send_mail(data):
    #     message = EmailMessage(
    #         subject=data.get('subject'), body=data.get('email_body'), to=[data.get('email')])
    #     message.send()

    @staticmethod
    def token_encode(token):
        token_string_bytes = token.encode("ascii")

        base64_bytes = base64.b64encode(token_string_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string

    @staticmethod
    def token_decode(token_):
        base64_bytes = token_.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string


def get_data(request):
    url_token = request.headers.get('Token')
    if not url_token:
        url_token = request.query_params.get('token')
    token = Common.token_decode(url_token)
    data = decode(token, settings.SECRET_KEY, 'HS256')
    user_data = data
    return user_data


# class Email():
#     def send_email(self):
#       email_body = {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': get_token,
#                 }
#
#                 link = reverse('activate', kwargs={
#                     'uidb64': email_body['uid'], 'token': email_body['token']})
#
#                 email_subject = 'Activate your account'
#
#                 activate_url = 'http://' + current_site.domain + link
#
# email = EmailMessage( email_subject, 'Hi ' + user.username + ', Please the Click the link below to activate your
# account \n' + activate_url, 'noreply@gmail.com', [email], ) email.send(fail_silently=False)


# def send_email(self, user):
#     mail_subject = 'Activation link has been sent to your email id'
#     current_site = get_current_site(request).domain
#     token = get_data(user).get('access')
#     short_token = Common.token_encode(token)
#     link = reverse('activate')
#     surl = 'http://' + current_site + link + '?token=' + short_token
#
#     message = render_to_string('acc_active_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': surl,
#     })
#     to_email = request.data.get('email')
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#     email.send()


def mail(request):
    subject = "Greetings"
    msg = "Congratulations for your success"
    # email = request.data.get('email')
    to = 'valarmathyb123@gmail.com'
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if res == 1:
        msg = "Mail Sent Successfuly"
    else:
        msg = "Mail could not sent"
    return HttpResponse(msg)
