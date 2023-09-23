# import jwt
# from django.conf import settings
# from rest_framework import exceptions
# from django.contrib.auth import authenticate, get_user_model
# from rest_framework import exceptions,status


# class TokenBlackListException(exceptions.APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = "Unauthorized User."

# def get_username_from_payload_handler(payload):
#     username = payload.get("username")
#     authenticate(username=username)
#     return username


# def create_jwt_token(user):
#     payload = {
#         'user_id': user.id,
#         'username': user.username,
#     }
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

# def decode_jwt_token(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise exceptions.AuthenticationFailed('Token has expired')
#     except jwt.DecodeError:
#         raise exceptions.AuthenticationFailed('Token decoding failed')


