from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Account
import requests


# Create your views here.

class AccountSerializer(serializers.ModelSerializer):

    class Meta :
        model = Account
        fields = '__all__'

class KakaoRequestSerializer(serializers.Serializer):
    accessToken = serializers.CharField()


class AccountView(APIView):
    @swagger_auto_schema(tags=['kakaoLogin'], operation_description='testing', request_body=KakaoRequestSerializer , responses={"200":"login", "201":"SignUp","400": "no token","404":"invalid token"})
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


        if (Account.objects.get(id=userData["id"])):
            user = Account.objects.get(id=userData["id"])
            serializer = AccountSerializer(user)
            return response.JsonResponse(serializer.data, status=200)
        else :
            account = Account.objects.create_user(userData=userData)
            serializer = AccountSerializer(account)
            return response.JsonResponse(serializer.data, status=201)
        
    def get(self, request):
        userid = request.GET.get('uid')
        try :
            profile = Account.objects.get(id=userid)
            serializer = AccountSerializer(profile)
            return response.JsonResponse(serializer.data, status=200)
        except:
            return response.HttpResponse(status=404)
