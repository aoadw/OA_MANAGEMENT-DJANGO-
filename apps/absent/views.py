from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.absent.models import Absent,AbsentType
from apps.absent.utils import get_responser
from apps.absent.serializers import AbsentSerializer, AbsentTypeSerializer
from apps.oaauther.serializers import UserSerializer


class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    # 创建考勤 create
    # 审批考勤 update
    # 查看自己考勤信息 ?who=my
    # 查看下属考勤信息 ?who=sub

    queryset = Absent.objects.all().order_by('id')
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 重写父类方法
        # 在DRF中，想要修改某一个数据，需要传入在序列化中指定的所有的字段
        # 如果不想传入，需要设置kwargs中的partial值为 True
        kwargs['partial'] = True
        # 调用父类update方法，以实现改动
        return super().update(request, *args, **kwargs)

    # 重写之后的list没有分页功能，分页功能也需要重写
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responser=request.user)
        else:
            result = queryset.filter(requester=request.user)

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response 除了返回序列化的数据，还返回总页数，下一页的url
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(result, many=True)
        return Response(data=serializer.data)


# 实现查看考勤类型
class AbsentTypesView(APIView):

    def get(self, request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types,many=True)
        return Response(serializer.data)


# 实现查看审批人
class ResponserView(APIView):

    def get(self, request):
        responser = get_responser(request)
        # serializer 如果序列化对象是None ，不会报错， 会返回一个空的字典（未设定默认值的为null，设定默认值的为默认值）
        serializer = UserSerializer(responser)
        return Response(serializer.data)