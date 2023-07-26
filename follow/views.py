from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

#jwt
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from config.exceptions import NoContentException

from django.http import response
from .models import Account, Follow
from account.views import ProfileSerializer


from config.util import Verify



class FollowSerializer(serializers.Serializer):
    id = serializers.CharField(default='admin')

class FollowView(APIView, JWTStatelessUserAuthentication):
    follower = openapi.Parameter('follower', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="ID's follower", default=2919921020)
    followee = openapi.Parameter('followee', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="ID's followee", default=2919921020)

    @swagger_auto_schema(tags=['follow'], manual_parameters=[follower, followee])
    def get(self, request):
        Verify.jwt(self, request=request)
        if request.GET.get('follower', default = None) != None and request.GET.get('followee') == None:
            key = request.GET.get('follower', default = None)
            follower = Follow.objects.filter(followee = key).values('follower')
            users = Account.objects.filter(id__in = follower)
            serializer = ProfileSerializer(users, many=True)
            return response.JsonResponse(serializer.data, safe=False)
            
        elif request.GET.get('followee', default = None) != None and request.GET.get('follower') == None:
            key = request.GET.get('followee', default = None)
            followee = Follow.objects.filter(follower = key).values('followee')
            users = Account.objects.filter(id__in = followee)
            serializer = ProfileSerializer(users, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        else:
            key_followee = request.GET.get('followee', default = None)
            key_follower = request.GET.get('follower', default = None)
            try: 
                Follow.objects.get(follower = key_follower, followee=key_followee)
                return response.JsonResponse({"detail":True})
            except:
                return response.JsonResponse({"detail":False})



    @swagger_auto_schema(tags=['follow'], request_body=FollowSerializer)      
    def post(self, request):
        user = Verify.jwt(self, request=request)
        try : 
            data_follower = Account.objects.get(id = user.id)
            data_followee = Account.objects.get(id = request.data.get('id'))
        except :
            raise NoContentException(detail="can't find user")

        try: 
            Follow.objects.get(follower = user.id, followee=data_followee)
            return response.JsonResponse({'detail':"already follow"}, status = 400)
        
        except :
            Follow.objects.create(
                follower = data_follower,
                followee = data_followee
            )
            return response.HttpResponse(status= 201)

    @swagger_auto_schema(tags=['follow'], request_body=FollowSerializer) 
    def delete(self, request):
        user = Verify.jwt(self, request=request)
        try : 
            id = request.data.get('id')
        except :
            raise NoContentException(detail="can't find user")

        if Follow.objects.filter(follower = user.id, followee=id):
            follow = Follow.objects.get(follower_id = user.id, followee_id=id)
            follow.delete()
            return response.HttpResponse(status=200)
        else:
            return response.JsonResponse({"status":"already unfollowed"}, status=200)