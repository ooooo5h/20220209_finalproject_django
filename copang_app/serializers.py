# queryset결과를 dict로 자동 변환해주는 기능

from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'