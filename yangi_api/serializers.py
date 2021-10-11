from rest_framework.fields import  SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import News, User



class NewsSerializer(ModelSerializer):
    content_count = SerializerMethodField()
    class Meta:
        model = News
        fields = ["id", "title", "content", "category", "content_count"]


    def get_content_count(self, obj):
        return len(obj.content)


# class UserSerializers(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "fullname", "username", "password"]

#     def is_valid(self, *args, **kwargs):
#         valid = False
#         if kwargs.get("username",None) and kwargs.get("password", None):
#             return True

    
