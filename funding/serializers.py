from rest_framework import serializers
from .models import Funding, Account
class FundingDetailSerializer(serializers.ModelSerializer):

    def getAuthor(self, obj):
        id = obj.author.id
        author = Account.objects.get(id = id)
        image = author.image.url if author.image else None
        profile = {
            "id" : author.id,
            "username" : author.username,
            "image" : image
        }
        return profile
    
    
    author = serializers.SerializerMethodField('getAuthor')

    class Meta :
        model = Funding
        fields = ['id', 'title', 'content', 'goal_amount', 'current_amount', 'image', 'expire_on', 'created_on', 'public', 'author', 'review', 'review_image']

class FundingSerializer(serializers.ModelSerializer):

    def getAuthor(self, obj):
        id = obj.author.id
        author = Account.objects.get(id = id)
        image = author.image.url if author.image else None
        profile = {
            "id" : author.id,
            "username" : author.username,
            "image" : image
        }
        return profile

    author = serializers.SerializerMethodField('getAuthor')

    class Meta:
        model = Funding
        fields = ['id', 'title','image', 'goal_amount', 'current_amount', 'expire_on', 'public', 'author']

class FundingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ['title', 'content', 'goal_amount', 'image', 'public', 'expire_on']

class FundingPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ['id', 'title', 'content', 'public', 'image', 'public']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funding
        fields = ['id', 'review', 'review_image']