import json
import os

import jwt
import requests
from django.contrib.auth import authenticate


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get(os.environ.get('AUTH0_DOMAIN') + '.well-known/jwks.json').json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = os.environ.get('AUTH0_DOMAIN')
    audience = os.environ.get('AUTH0_DOMAIN') + 'userinfo'
    result = jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])
    return result


def get_decoded_token(request):
    token_parts = request.headers['Authorization']
    token = token_parts.split()[1]
    decoded_token = jwt_decode_token(token)
    return decoded_token


def get_user_id(decoded_token):
    user_id = decoded_token['sub'].replace('|', '.')
    return user_id


def get_user_role(decoded_token):
    user_role = decoded_token['http://schemas.microsoft.com/ws/2008/06/identity/claims/role']
    return user_role[0]
