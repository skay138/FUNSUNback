from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Funding
# Create your views here.

from config.util import Verify


class FundingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funding
        fields = '__all__' + 'uid'



class FundingView(APIView):

    #펀딩 id로 게시물 찾기
    def get(self, request):
        funding = Verify.funding(request=request)
        if(type(funding)==response.HttpResponse):
            return funding
        
        serializer = FundingSerializer(funding)
        return response.JsonResponse(serializer.data, status=200)

    #생성
    def post(self, request):
        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author

        goal_amount = int(request.data.get('goal_amount'))

        if(goal_amount > 10000000 or goal_amount < 1000):
            return response.HttpResponse(status=405)
        else:
            funding = Funding.objects.create(
                goal_amount=goal_amount,
                author=author
            )
            
            for keys in request.data:
                if hasattr(funding, keys)== True:
                    if(keys == 'goal_amount'):
                        pass
                    elif(keys == 'author'):
                        pass
                    else:
                        setattr(funding, keys, request.data[keys])
            funding.save()
            serializer = FundingSerializer(funding)
            return response.JsonResponse(serializer.data, status=200)

    def put(self, request):
        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author
        funding = Verify.funding(request=request)
        if(type(funding)==response.HttpResponse):
            return funding

        if(funding.author == author):
            for keys in request.data:
                if hasattr(funding, keys) == True:
                    if(keys == 'goal_amount'):
                        pass
                    elif(keys == 'author'):
                        pass
                    elif(keys == 'current_amount'):
                        pass
                    else:
                        setattr(funding, keys, request.data[keys])
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)
        
    #삭제
    def delete(self, request):

        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author
        funding = Verify.funding(request=request)
        if(type(funding)==response.HttpResponse):
            return funding

        if(funding.author == author):
            funding.delete()
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)