from rest_framework import serializers
from .models import Account
from follow.models import Follow


class ProfileSerializer(serializers.ModelSerializer):

    def getFollower(self, obj):
        id = obj.id
        follwer = Follow.objects.filter(followee = id).count()
        return follwer

    def getFollowee(self, obj):
        id = obj.id
        followee = Follow.objects.filter(follower = id).count()
        return followee

    follower = serializers.SerializerMethodField('getFollower')
    followee = serializers.SerializerMethodField('getFollowee')

    class Meta :
            model = Account
            fields = ['id', 'email', 'birthday', 'username', 'image', 'follower', 'followee']


class AccountSerializer(serializers.ModelSerializer):
    class Meta :
        model = Account
        fields = ['id', 'email', 'birthday', 'username', 'image', 'gender']

class KakaoRequestSerializer(serializers.Serializer):
    accessToken = serializers.CharField()
