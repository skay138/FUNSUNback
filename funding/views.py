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
from remit.models import Remit
from follow.models import Follow
# Create your views here.

from config.util import OverwriteStorage, Verify, funding_image_upload, review_image_upload, paging_funding


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

    class Meta:
        model = Funding
        fields = ['id', 'title','image', 'goal_amount', 'current_amount', 'expire_on']

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


class FundingView(APIView, JWTStatelessUserAuthentication):
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    #펀딩 id로 게시물 찾기
    @swagger_auto_schema(manual_parameters=[id], operation_description='GET FUNDING INFO')
    def get(self, request):
        Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)
        serializer = FundingDetailSerializer(funding)
        return response.JsonResponse(serializer.data, status=200)

    #생성
    @swagger_auto_schema(operation_description='testing', request_body=FundingPostSerializer)
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
            serializer = FundingDetailSerializer(funding)
            return response.JsonResponse(serializer.data, status=201)
        
    
    @swagger_auto_schema(operation_description='testing', request_body=FundingPutSerializer)
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
            serializer = FundingDetailSerializer(funding)
            return response.JsonResponse(serializer.data, status=200)
        else:
            return response.JsonResponse({"detail":"not author"},status=400)
        
    #삭제
    @swagger_auto_schema(request_body=FundingPutSerializer)
    def delete(self, request):
        author = Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)

        if(funding.author.id == author.id):
            funding.delete()
            return response.HttpResponse(status=200)
        else:
            return response.JsonResponse({"detail":"bad request"},status=400)
        
class reviewFunding(APIView, JWTStatelessUserAuthentication):
    @swagger_auto_schema(request_body=ReviewSerializer)
    def post(self, request):
        author = Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)

        if(funding.author.id == author.id):
            funding.review = request.data.get('review')
            if(request.FILES.get('review_image')):
                data_image = request.FILES.get('review_image')
                setattr(funding, 'review_image', OverwriteStorage().save(review_image_upload(funding.id), data_image))
            funding.save()
            serializer = FundingDetailSerializer(funding)
        return response.JsonResponse(serializer.data, status=200)
        

# class GetMyFundings(APIView, JWTStatelessUserAuthentication):
#     page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
#     @swagger_auto_schema(manual_parameters=[page], operation_description='GET MY FUNDING')
#     def get(self, request):
#         user = Verify.jwt(self, request=request)
#         fundings = Funding.objects.filter(author_id = user.id).order_by('-id')
#         paginator = paging_funding(request=request, list=fundings)
#         serializer = FundingSerializer(paginator, many=True)
#         return response.JsonResponse(serializer.data, safe=False, status=200)
    
class GetFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='admin')
    @swagger_auto_schema(manual_parameters=[page, id], operation_description='GET USER FUNDINGS')
    def get(self, request):
        user = Verify.jwt(self, request=request)
        fundinguser = request.GET.get('id')
        if user.id == fundinguser:
            fundings = Funding.objects.filter(author_id = user.id).order_by('-id')
            paginator = paging_funding(request=request, list=fundings)
            serializer = FundingSerializer(paginator, many=True)
            return response.JsonResponse(serializer.data, safe=False, status=200)
        else :
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
        fundings = Funding.objects.filter(public = True).order_by('-id')
        paginator = paging_funding(request=request, list=fundings)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    



