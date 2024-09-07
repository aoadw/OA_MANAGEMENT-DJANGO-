from rest_framework import serializers
from django.core.validators import FileExtensionValidator


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
        error_messages={'invalid_image': '请上传正确的图片格式！',
                        'required': '请上传图片！'}
    )

    def validate_image(self, value):
        max_size = 0.5 * 1024 * 1024  # 最大上传0.5MB 图片
        size = value.size
        if size > max_size:
            raise serializers.ValidationError({'图片上传大小应在0.5MB之内'})
        return value
