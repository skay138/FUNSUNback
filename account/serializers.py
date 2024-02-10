from rest_framework import serializers
from .models import Account
from follow.models import Follow


class ProfileSerializer(serializers.ModelSerializer):

    class Meta :
            model = Account
            fields = ['id', 'email', 'birthday', 'username', 'image', 'follower_count', 'followee_count']


class MyProfileSerializer(serializers.ModelSerializer):

    class Meta :
            model = Account
            fields = ['id', 'email', 'birthday', 'username', 'image', 'follower_count', 'followee_count', 'bank_account']


class AccountSerializer(serializers.ModelSerializer):
    class Meta :
        model = Account
        fields = ['id', 'email', 'birthday', 'username', 'image', 'gender', 'bank_account']

class KakaoRequestSerializer(serializers.Serializer):
    accessToken = serializers.CharField()
