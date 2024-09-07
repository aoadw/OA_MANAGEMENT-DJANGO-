from django.shortcuts import render
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer,UserSerializer,UserPwdSerializer
from . import authenicitions


class LoginView(APIView):

    def post(self, request):
        # 1 . 使用 模型序列化 验证数据是否可用
        login_serializer = LoginSerializer(data=request.data)

        if login_serializer.is_valid():     # 如果验证通过
            user = login_serializer.validated_data.get('user')  # validated_data的返回值即为attrs，通过这个获取user对象
            user.last_login = datetime.now()                    # 修改登录时间为当前时间
            user.save()                                         # 修改完后保存

            token = authenicitions.get_token(user)              # 获取token
            return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            detail = list(login_serializer.errors.values())[0][0]
            print(login_serializer.errors)
            # drm中错误信息 是 detail
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePwdView(APIView):

    def post(self, request):
        # request是DRF中的Request对象
        # request._request拿到django自带的request对象
        # print(request)
        # print(request.user)

        # 使用context将request对象传给serializer
        pwd_serializer = UserPwdSerializer(data=request.data,context={'request': request})

        if pwd_serializer.is_valid():
            request.user.set_password(pwd_serializer.validated_data.get('new_password'))
            request.user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(pwd_serializer.errors)
            detail = list(pwd_serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)
