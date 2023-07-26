from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

#jwt
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from django.db.models import Q
from django.http import response
from .models import Funding, Account
from remit.models import Remit
from follow.models import Follow
# Create your views here.

from config.util import OverwriteStorage, Verify, funding_image_upload, paging_funding


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
                    elif(keys == 'current_amount'):
                        pass
                    elif keys == 'image' and request.FILES.get('image'):
                        data_image = request.FILES.get('image')
                        setattr(funding, keys, OverwriteStorage().save(funding_image_upload(funding.id), data_image))
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
                    elif(keys == 'expire_on'):
                        pass
                    elif keys == 'image' and request.FILES.get('image'):
                        data_image = request.FILES.get('image')
                        setattr(funding, keys, OverwriteStorage().save(funding_image_upload(funding.id), data_image))
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
        

class GetMyFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET MY FUNDING')
    def get(self, request):
        user = Verify.jwt(self, request=request)
        fundings = Funding.objects.filter(author_id = user.id).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    
class GetUserFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='admin')
    @swagger_auto_schema(manual_parameters=[page, id], operation_description='GET USER FUNDINGS')
    def get(self, request):
        user = Verify.jwt(self, request=request)
        fundinguser = request.GET.get('id')
        isFriend = Follow.objects.filter(follower = user.id, followee = fundinguser).count() & Follow.objects.filter(follower = fundinguser, followee=user.id).count()
        fundings = Funding.objects.filter(author_id = fundinguser).order_by('-id') if isFriend else Funding.objects.filter(author_id = fundinguser, public=True).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)

class GetFollowFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET FOLLOW FUNDING')
    def get(self, request):

        user = Verify.jwt(self, request=request)
        followee = Follow.objects.filter(follower = user.id).values('followee')
        friend = Follow.objects.filter(followee = user.id , follower__in = followee).values('follower')
        print(friend)
        fundings = Funding.objects.filter(author__in = followee, public = True).order_by('-id') | Funding.objects.filter(author__in = friend, public=False).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    

class GetJoinedFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET JOINED FUNDING')
    def get(self, request):
        user = Verify.jwt(self, request=request)
        funding_ids = Remit.objects.filter(author_id = user.id).values('funding').distinct()
        fundings = Funding.objects.filter(id__in = funding_ids).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)


class GetPublicFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET PUBLIC FUNDING')
    def get(self, request):
        Verify.jwt(self, request=request)
        fundings = Funding.objects.filter(public = True).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    



