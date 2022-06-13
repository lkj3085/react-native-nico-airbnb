from django.contrib.auth.models import User
import jwt
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")
            decode = jwt.encode(
                jwt_token, settings.SECRET_KEY, algorithm=["HS256"])
            pk = decode.get('pk')
            user = User.objects.get(pk=pk)
            return user
        except ValueError:
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT FORMAT INVALID")
        except User.DoesNotExist:
            return None
