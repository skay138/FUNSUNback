from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Account, Follow
from account.views import AccountSerializer


from config.util import Verify



class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = "__all__"

class FollowView(APIView):
    follower = openapi.Parameter('follower', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="ID's follower", default=2919921020)
    followee = openapi.Parameter('followee', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="ID's followee", default=2919921020)

    @swagger_auto_schema(tags=['follow'], manual_parameters=[follower, followee])
    def get(self, request):
        if request.GET.get('follower', default = None) != None and request.GET.get('followee') == None:
            key = request.GET.get('follower', default = None)
            follower = Follow.objects.filter(followee = key).values('follower')
            users = Account.objects.filter(id__in = follower)
            serializer = AccountSerializer(users, many=True)
            return response.JsonResponse(serializer.data, safe=False)
            
        elif request.GET.get('followee', default = None) != None and request.GET.get('follower') == None:
            key = request.GET.get('followee', default = None)
            followee = Follow.objects.filter(follower = key).values('followee')
            users = Account.objects.filter(id__in = followee)
            serializer = AccountSerializer(users, many=True)
            return response.JsonResponse(serializer.data, safe=False)
        else:
            key_followee = request.GET.get('followee', default = None)
            key_follower = request.GET.get('follower', default = None)
            try: 
                Follow.objects.get(follower = key_follower, followee=key_followee)
                return response.JsonResponse({"status":"true"})
            except:
                return response.JsonResponse({"status":"false"})



    @swagger_auto_schema(tags=['follow'], request_body=FollowSerializer)      
    def post(self, request):
        try : 
            data_follower = Account.objects.get(id = request.data.get('follower'))
            data_followee = Account.objects.get(id = request.data.get('followee'))
        except :
            return response.JsonResponse({"status" : "follow user not found"}, status=400)

        try: 
            Follow.objects.get(follower = data_follower, followee=data_followee)
            return response.JsonResponse({'status':"already follow"}, status = 201)
        except :
            Follow.objects.create(
                follower = data_follower,
                followee = data_followee
            )
            return response.JsonResponse({"status":"good"}, status= 200)

    @swagger_auto_schema(tags=['follow'], request_body=FollowSerializer) 
    def delete(self, request):
        try : 
            data_follower = Account.objects.get(id = request.data.get('follower'))
            data_followee = Account.objects.get(id = request.data.get('followee'))
        except :
            return response.JsonResponse({"status" : "follow user not found"}, status=400)

        if Follow.objects.filter(follower = data_follower, followee=data_followee):
            follow = Follow.objects.get(follower = data_follower, followee=data_followee)
            follow.delete()
            return response.JsonResponse({"status":"good"}, status=200)
        else:
            return response.JsonResponse({"status":"already unfollowed"}, status=200)