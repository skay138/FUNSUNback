from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

#jwt
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from django.http import response
from .models import Funding, Account
# Create your views here.

from config.util import Verify


class FundingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funding
        fields = '__all__'



class FundingView(APIView, JWTStatelessUserAuthentication):
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    #펀딩 id로 게시물 찾기
    @swagger_auto_schema(manual_parameters=[id], operation_description='GET FUNDING INFO')
    def get(self, request):
        Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)
        serializer = FundingSerializer(funding)
        return response.JsonResponse(serializer.data, status=200)

    #생성
    @swagger_auto_schema(operation_description='testing', request_body=FundingSerializer)
    def post(self, request):
        author = Verify.jwt(self, request=request)
        goal_amount = int(request.data.get('goal_amount'))

        if(goal_amount > 10000000 or goal_amount < 1000):
            return response.JsonResponse({"detail":"out value"},status=400)
        else:
            funding = Funding.objects.create(
                goal_amount=goal_amount,
                author=Account.objects.get(id=author.id)
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
        
    
    @swagger_auto_schema(operation_description='testing', request_body=FundingSerializer)
    def put(self, request):
        author = Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)

        if(funding.author.id == author.id):
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
            funding.save()
            return response.HttpResponse(status=200)
        else:
            return response.JsonResponse({"detail":"not author"},status=400)
        
    #삭제
    def delete(self, request):
        author = Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)

        if(funding.author.id == author.id):
            funding.delete()
            return response.HttpResponse(status=200)
        else:
            return response.JsonResponse({"detail":"bad request"},status=400)