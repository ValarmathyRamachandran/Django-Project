from django.utils.baseconv import base64
from jwt import decode
from django.conf import settings
from rest_framework.response import Response


def true_token(token_):
    base64_bytes = token_.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


class TokenRequired(Exception):
    pass


def token_required(request):
    try:
        short_token = request.headers.get('access-token')
        if not short_token:
            short_token = request.query_params.get('access-token')
        if not short_token:
            raise TokenRequired(404)
        index = short_token.find('.')

        if index == -1:
            token = true_token(short_token)
        else:
            token = short_token
        data = decode(token, settings.SECRET_KEY, 'HS256')
        user_id = data['user_id']
        return user_id
    except Exception as e:
        return dict({'Error': str(e), 'Code': 404})


# def token_required(f):
#     def decorated(request, *args, **kwargs):
#         token = request.headers.get('access-token')
#         # jwt is passed in the request header
#         if 'access-token' in request.headers:
#             token = request.query_params.get['access-token']
#         # return 401 if token is not passed
#         if not token:
#             return Response({'msg': 'Token is missing !!'}), 401
#
#         index = token.find('.')
#
#         if index == -1:
#             access_token = true_token(token)
#         else:
#             access_token = token
#         data = decode(access_token, settings.SECRET_KEY, 'HS256')
#         user_id = data['user_id']
#         return f(request, user_id, *args, **kwargs)
#     return decorated
