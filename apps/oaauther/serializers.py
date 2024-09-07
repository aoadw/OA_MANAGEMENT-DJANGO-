from rest_framework import serializers
from .models import OAUser,UserStatusChoices,OADepartment
from rest_framework import exceptions



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True,min_length=6,max_length=20)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("邮箱错误或不存在")
            if not user.check_password(password):   # 邮箱检查存在后检查密码是否正确
                # 密码错误返回错误
                raise serializers.ValidationError("密码错误")
            # 判断用户状态
            if user.status == UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError('该用户未激活')
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError('该用户已锁定')
            # 四个校验都通过执行以下代码
            # 简化查询，将序列化中获取的user对象返回，就不需要视图函数中在查询获取一次
            attrs['user'] = user
        else:
            raise serializers.ValidationError('需要传入邮箱和密码')

        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = OAUser
        exclude = ('password', 'groups', 'user_permissions')


class UserPwdSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,min_length=6,max_length=20)
    new_password = serializers.CharField(required=True,min_length=6,max_length=20)
    acc_password = serializers.CharField(required=True,min_length=6,max_length=20)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        acc_password = attrs.get('acc_password')
        # 丛视图函数中传进来的request对象
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise exceptions.ValidationError('旧密码与原密码不一致')
        if new_password != acc_password:
            raise exceptions.ValidationError('新密码与确认密码不一致')
        return attrs
