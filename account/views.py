from typing import Any
from django.shortcuts import render

#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

#jwt
from config.jwt import MyTokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

#model/serializer
from .models import Account
from .serializers import AccountSerializer, ProfileSerializer, KakaoRequestSerializer

#http
from django.http import response
import requests

#utils
from config.util import Verify, OverwriteStorage, image_upload


# Create your views here.


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
                'username':kakao_response["kakao_account"]["profile"]["nickname"],
                'gender':kakao_response["kakao_account"]['gender'],
                'age_range':kakao_response["kakao_account"]['age_range'],
                'birthday' :kakao_response["kakao_account"]['birthday'],
                'email':kakao_response["kakao_account"]['email']
            }
            print(userData)
        except :
            return response.JsonResponse({"detail":"userData not found"},status=404)
        
        try :
            account = Account.objects.get(id = userData['id'])
            serializer = ProfileSerializer(account)
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

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='admin')

    @swagger_auto_schema(operation_description='get my profile')
    def post(self, request):
        user = Verify.jwt(self, request=request)
        account = Account.objects.get(id=user.id)
        serializer = ProfileSerializer(account)
        return response.JsonResponse(serializer.data)
        


    @swagger_auto_schema(manual_parameters=[id], operation_description='GET USER INFO')
    def get(self, request):
        Verify.jwt(self, request=request)
        account = Verify.account(request=request)
        serializer = ProfileSerializer(account)
        return response.JsonResponse(serializer.data, status=200)
    
    
    @swagger_auto_schema(operation_description='testing', request_body=AccountSerializer)
    def put(self, request):
        user = Verify.jwt(self, request=request)
        profile = Account.objects.get(id=user.id)
        for keys in request.data:
            if hasattr(profile, keys)== True:
                if keys == 'is_superuser':
                    pass
                if keys == 'is_staff':
                    pass
                if keys == 'image' and request.FILES.get('image'):
                    data_image = request.FILES.get('image')
                    setattr(profile, keys, OverwriteStorage().save(image_upload(user.id), data_image))
                else :
                    setattr(profile, keys, request.data[keys])
        profile.save()
        serializer = ProfileSerializer(profile)
        return response.JsonResponse(serializer.data, status=200)
    
    @swagger_auto_schema(request_body=AccountSerializer)
    def delete(self, request):
        user = Verify.jwt(self, request=request)
        try :
            profile = Account.objects.get(id=user.id)
            profile.delete()
            return response.HttpResponse(status=200)
        except Account.DoesNotExist:
            return response.JsonResponse({"detail":"already deleted"}, status=208)
        except:
            return response.JsonResponse({'detail':"Bad request"}, status=400)
        

class ProfileSearch(APIView, JWTStatelessUserAuthentication):
    username = openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='admin')
    @swagger_auto_schema(manual_parameters=[username], operation_description='SEARCH USERS')
    def get(self, request):
        Verify.jwt(self, request=request)
        profile = Account.objects.filter(username__contains = request.GET.get('username'))
        serializer = ProfileSerializer(profile, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    


class GetToken(APIView):
    def get(self, request):
        account = Account.objects.get(id = 'admin')
        serializer = ProfileSerializer(account)
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