from rest_framework.serializers import ModelSerializer

from users.models import Admin


class AdminSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
