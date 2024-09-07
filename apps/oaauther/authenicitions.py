import jwt
import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from .models import OAUser


def get_token(user):                            # 获取token函数
    timestamp = time.time() + 60*60*24*7        # 过期时间为7天
    key = settings.SECRET_KEY
    token = jwt.encode({'userid':user.uuid,'exp':timestamp},key,algorithm='HS256')
    return token


class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 这里的request对象是DRF的Request对象
        return request._request.user, request._request.auth


class JWTAuthentication(BaseAuthentication):
    """
       Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'JWT'
    model = None

    def authenticate(self, request):

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = '没有提供Token.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = '无效的JWT.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            # 解码编码的key和格式要一致
            jwt_token = auth[1]
            payload = jwt.decode(jwt_token.decode(),settings.SECRET_KEY,algorithms=['HS256'])
            userid = payload.get('userid')
            try:
                user = OAUser.objects.get(pk=userid)
                return user,jwt_token
            except Exception:
                msg = '用户不存在'
                raise exceptions.AuthenticationFailed(msg)

        except UnicodeError:
            msg = '无效token.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = '已过期.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = '无效字段'
            raise exceptions.AuthenticationFailed(msg)




