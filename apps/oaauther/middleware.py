from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework import status
from rest_framework import exceptions
import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import OAUser


class LoginCheckMiddleware(MiddlewareMixin):

    keyword = "JWT"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 设置白名单
        self.white_path = ['/auth/login/']

    def process_request(self, request):
        if request.path in self.white_path or request.path.startswith(settings.MEDIA_URL):
            request.user = AnonymousUser()
            request.auth = None
            return None

        try:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('请传入JWT！')

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
                    # request是django中的HttpRequest对象
                    request.user = user
                    request.auth = jwt_token

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

        except Exception as e:
            print(e)
            return JsonResponse({'detail':'请先登录'},status=status.HTTP_403_FORBIDDEN)
