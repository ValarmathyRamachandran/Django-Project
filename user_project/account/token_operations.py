from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.baseconv import base64
from jwt import decode
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


class Common:
    @staticmethod
    def send_mail(data):
        message = EmailMessage(
            subject=data.get('subject'), body=data.get('email_body'), to=[data.get('email')])
        message.send()

    def true_token(token_):
        base64_bytes = token_.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string


def get_user(request):
    url_token = request.headers.get('Token')
    if not url_token:
        url_token = request.query_params.get('token')
    token = Common.true_token(url_token)
    data = decode(token, settings.SECRET_KEY, 'HS256')
    user_id = data['user_id']
    return user_id

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
