from rest_framework import serializers

from .models import Books


'''
DRF ModelSerializer 会根据模型字段自动生成以下验证：

字段属性	自动验证内容
blank=False	不允许为空字符串（表单）
null=False	不允许为 None
max_length=100	限制最大字符数
unique=True	自动校验唯一性
choices	限制只能为列出的选项


单字段验证	validate_<field_name>(self, value)
多字段验证	validate(self, attrs)
全局函数验证器	validators=[my_func]
手动触发验证	serializer.is_valid()
验证失败返回	serializer.errors
'''
def not_hello(value):
    if value.lower() == 'hello':
        raise serializers.ValidationError("不能是hello")
    return value


class BooksSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators= [not_hello])
    class Meta:
        model = Books
        fields = "__all__"

    # 针对单个字段的验证,这里是验证title
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("标题太短")
        return value
    
    # 所有的验证都经过这里,
    def validate(self, attrs):
        if attrs['title'] < 5:
            raise serializers.ValidationError("标题太短2")
        if attrs['content'] == 0:
            raise serializers.ValidationError("没有内容")
        return attrs




