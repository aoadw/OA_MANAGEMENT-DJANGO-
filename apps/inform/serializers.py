from rest_framework import serializers
from apps.oaauther.serializers import UserSerializer,DepartmentSerializer
from apps.inform.models import Inform
from apps.oaauther.models import OADepartment


class InformSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    departments = DepartmentSerializer(read_only=True, many=True)
    # 如果后端要接受列表，使用ListField
    # department_ids 是一个包含了部门id的列表
    department_ids = serializers.ListField(write_only=True)

    class Meta:
        model = Inform
        fields = '__all__'
        read_only_fields = ('public',)

    def create(self, validated_data):
        request = self.context.get('request')
        department_ids = validated_data.pop('department_ids')
        department_ids = list(map(lambda value: int(value), department_ids))
        if 0 in department_ids:
            inform = Inform.objects.create(public=True,author=request.user,**validated_data)
        else:
            departments = OADepartment.objects.filter(id__in=department_ids).all()
            inform = Inform.objects.create(public=False,author=request.user,**validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform
