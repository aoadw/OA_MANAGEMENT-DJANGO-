from rest_framework import serializers
from apps.absent.models import Absent,AbsentType,AbsentStatusChoices
from apps.oaauther.serializers import UserSerializer
from rest_framework import exceptions

from .utils import get_responser


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    # read_only  只在将ORM模型序列化成字典时，会将这个字段序列化
    # write_only 只在将data进行校验时会用到
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only=True)
    responser = UserSerializer(read_only=True)

    class Meta:
        model = Absent
        fields = '__all__'

    def validate_absent_type_id(self, value):
        # 判断类型是否存在，如果不存在抛出异常
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError('类型不存在')
        return value

    def create(self, validated_data):
        request = self.context['request']

        responser = get_responser(request)

        if responser is None:
            validated_data['status'] = AbsentStatusChoices.PASS
        else:
            validated_data['status'] = AbsentStatusChoices.AUDITING

        absent = Absent.objects.create(**validated_data,requester=request.user,responser=responser)
        return absent

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail='已审核完毕，无法修改')
        request = self.context['request']
        user = request.user
        if instance.responser.uuid != user.uuid:
            raise exceptions.AuthenticationFailed(detail='无权审理')
        instance.status = validated_data['status']
        instance.response_context = validated_data['response_context']
        instance.save()
        return instance
