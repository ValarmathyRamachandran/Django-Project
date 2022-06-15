from functools import wraps

from django.utils.baseconv import base64
from jwt import decode
from django.conf import settings
from rest_framework.response import Response


def true_token(token_):
    base64_bytes = token_.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


def token_required(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        short_token = request.headers.get('access-token')
        if not short_token:
            short_token = request.query_params.get('access-token')
        if not short_token:
            return {'msg': 'Token is missing!', 'code': 409}
        index = short_token.find('.')
        # data = decode(token.split()[1], settings.SECRET_KEY, 'HS256')
        if index == -1:
            token = true_token(short_token)
        else:
            token = short_token
        data = decode(token, settings.SECRET_KEY, 'HS256')
        user_id = data['user_id']
        return f(request, user_id, *args, **kwargs)

    return decorated
