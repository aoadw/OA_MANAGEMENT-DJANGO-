from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageSerializer
from shortuuid import uuid
import os
from django.conf import settings


class UploadImageView(APIView):

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data.get('image')
            image_name = uuid() + os.path.splitext(image.name)[-1]
            path = os.path.join(settings.MEDIA_ROOT, image_name)  # 使用 os.path.join 拼接路径

            try:
                with open(path, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

            except Exception as e:
                print(f"Error saving image: {e}")  # 打印错误信息以便调试
                return Response({
                    "errno": 1,
                    "message": '图片保存失败!'
                })

            url = settings.MEDIA_URL + image_name  # 拼接 URL

            return Response({
                "errno": 0,
                "data": {
                    "url": url,
                    "alt": "",
                    "href": url
                },
            })
        else:

            detail = list(serializer.errors.values())[0][0]
            print(detail)
            return Response({
                "errno": 1,
                "detail": detail
            })
