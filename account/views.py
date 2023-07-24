from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Account
import requests

from config.util import Verify


# Create your views here.

class AccountSerializer(serializers.ModelSerializer):
    class Meta :
        model = Account
        fields = '__all__'

class KakaoRequestSerializer(serializers.Serializer):
    accessToken = serializers.CharField()


class AccountView(APIView):
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=2919921020)


    @swagger_auto_schema(operation_description='testing', request_body=KakaoRequestSerializer)
    def post(self, request):
        try:
            token = request.data['accessToken']
            header = {
                "Authorization": "Bearer " + token
            }     
            kakao_response = requests.get("https://kapi.kakao.com/v2/user/me", headers=header).json()
        except:
            return response.HttpResponse(status=400)

        try:
            userData = {
                'id' : kakao_response["id"],
                'nickname':kakao_response["kakao_account"]["profile"]["nickname"],
                'gender':kakao_response["kakao_account"]['gender'],
                'age_range':kakao_response["kakao_account"]['age_range'],
                'birthday' :kakao_response["kakao_account"]['birthday'],
                'email':kakao_response["kakao_account"]['email'],
            }
            print(userData)
        except :
            return response.HttpResponse(status=404)

        try :
            user = Account.objects.get(id=userData["id"])
            serializer = AccountSerializer(user)
            return response.JsonResponse(serializer.data, status=200)
        except Account.DoesNotExist :
            account = Account.objects.create_user(userData=userData)
            serializer = AccountSerializer(account)
            return response.JsonResponse(serializer.data, status=201)
        
        
    @swagger_auto_schema(manual_parameters=[id], operation_description='GET USER INFO')
    def get(self, request):
        account = Verify.account(request=request)
        if(type(account)==response.HttpResponse):
            return account
        
        serializer = AccountSerializer(account)
        return response.JsonResponse(serializer.data, status=200)
        
    @swagger_auto_schema(operation_description='testing', request_body=AccountSerializer , responses={"200":"login", "201":"SignUp","400": "no token","404":"invalid token"})
    def put(self, request):
        userid = request.data.get('id')

        profile = Account.objects.get(id=userid)
        
        for keys in request.data:
            if hasattr(profile, keys)== True:
                if keys == 'is_admin':
                    pass
                setattr(profile, keys, request.data[keys])
        profile.save()
        serializer = AccountSerializer(profile)
        return response.JsonResponse(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountSerializer)
    def delete(self, request):
        if(request.data.get('id')):
            userid = request.data.get('id')
            try :
                profile = Account.objects.get(id=userid)
                profile.delete()
                return response.HttpResponse(status=200)
            except:
                return response.HttpResponse(status=300)
        else:
            return response.HttpResponse(status=404)
        


