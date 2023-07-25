from typing import Any
from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

#jwt
from config.jwt import MyTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

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


class KakaoLogin(APIView):

    @swagger_auto_schema(operation_description='testing', request_body=KakaoRequestSerializer)
    def post(self, request):
        try:
            token = request.data['accessToken']
            header = {
                "Authorization": "Bearer " + token
            }     
            kakao_response = requests.get("https://kapi.kakao.com/v2/user/me", headers=header).json()
        except:
            return response.JsonResponse({'detail':'kakaoToken error'},status=400)

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
            return response.JsonResponse({"detail":"userData not found"},status=404)
        
        try :
            account = Account.objects.get(id = userData.id)
            serializer = AccountSerializer(account)
            token = MyTokenObtainPairSerializer.get_token(account)
            acessToken = token.access_token
            data = {
                "user" : serializer.data,
                "token" : {
                    "access_token":str(acessToken),
                    "refresh_token":str(token)
                }
                
            }
            return response.JsonResponse(data, status=200)
            
        except Account.DoesNotExist:
            account = Account.objects.create_user(userData=userData)
            serializer = AccountSerializer(account)
            token = MyTokenObtainPairSerializer.get_token(account)
            acessToken = token.access_token
            data = {
                "user" : serializer.data,
                "token" : {
                    "access_token":str(acessToken),
                    "refresh_token":str(token)
                }
                
            }
            
            return response.JsonResponse(data, status=201)


class AccountView(APIView, JWTStatelessUserAuthentication):
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=2919921020)


    @swagger_auto_schema(operation_description='you can get test jwt from here !')
    def post(self, request):
            account = Account.objects.get(id = 'admin')
            serializer = AccountSerializer(account)
            token = MyTokenObtainPairSerializer.get_token(account)
            acessToken = token.access_token
            data = {
                "user" : serializer.data,
                "token" : {
                    "access_token":str(acessToken),
                    "refresh_token":str(token)
                }   
            }
            return response.JsonResponse(data, status=200)
        


    @swagger_auto_schema(manual_parameters=[id], operation_description='GET USER INFO')
    def get(self, request):
        Verify.jwt(self, request=request)
        account = Verify.account(request=request)
        serializer = AccountSerializer(account)
        return response.JsonResponse(serializer.data, status=200)
        
    @swagger_auto_schema(operation_description='testing', request_body=AccountSerializer , responses={"200":"login", "201":"SignUp","400": "no token","404":"invalid token"})
    def put(self, request):
        userid = Verify.jwt(self, request=request)
        profile = Account.objects.get(id=userid)
        
        for keys in request.data:
            if hasattr(profile, keys)== True:
                if keys == 'is_superuser':
                    pass
                if keys == 'is_staff':
                    pass
                setattr(profile, keys, request.data[keys])
        profile.save()
        serializer = AccountSerializer(profile)
        return response.JsonResponse(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountSerializer)
    def delete(self, request):
        userid = Verify.jwt(self, request=request)
        try :
            profile = Account.objects.get(id=userid)
            profile.delete()
            return response.HttpResponse(status=200)
        except Account.DoesNotExist:
            return response.JsonResponse({"detail":"already deleted"}, status=208)
        except:
            return response.JsonResponse({'detail':"Bad request"}, status=400)



