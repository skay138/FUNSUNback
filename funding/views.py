from django.shortcuts import render
from .serializers import FundingSerializer, FundingDetailSerializer, FundingPostSerializer, FundingPutSerializer, ReviewSerializer
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

from config.util import OverwriteStorage, Verify, funding_image_upload, review_image_upload, paging_funding,manual_pagination
from django.db.models import Q
import os



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
        public = request.data.get('public')
        if(public == 'true'):
            public = True
        if(public == 'false'):
            public =False

        if(goal_amount > 10000000 or goal_amount < 1000):
            return response.JsonResponse({"detail":"out value"},status=400)
        else:
            funding = Funding.objects.create(
                goal_amount=goal_amount,
                author=Account.objects.get(id=author.id),
                public = public
            )

            
            for keys in request.data:
                if hasattr(funding, keys)== True:
                    if(keys == 'goal_amount'):
                        pass
                    elif(keys == 'author'):
                        pass
                    elif(keys == 'current_amount'):
                        pass
                    elif(keys == 'public'):
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
        public = request.data.get('public')
        public = request.data.get('public')
        if(public == 'true'):
            public = True
        if(public == 'false'):
            public =False

        if(funding.author.id == author.id):
            for keys in request.data:
                if hasattr(funding, keys) == True:
                    if(request.data.get('image_delete') == 'delete'):
                        funding.image = None
                    if(request.data.get('image_delete') == 'delete'):
                        funding.image = None
                    if(keys == 'goal_amount'):
                        pass
                    elif(keys == 'author'):
                        pass
                    elif(keys == 'current_amount'):
                        pass
                    elif(keys == 'expire_on'):
                        pass
                    elif(keys == 'public'):
                        funding.public = public
                    elif keys == 'image' and request.FILES.get('image'):
                        data_image = request.FILES.get('image')
                        setattr(funding, keys, OverwriteStorage().save(funding_image_upload(funding.id), data_image))
                    else:
                        setattr(funding, keys, request.data[keys])
            funding.save()
            if(request.data.get('image_delete') == 'delete'):
                os.remove(f"media/funding_image/{funding.id}.png")
                
                
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
        target_id = request.GET.get('id')
        if user.id == target_id:
            fundings = Funding.objects.filter(author_id = user.id).order_by('-id').select_related('author')
            paginator = paging_funding(request=request, list=fundings)
            serializer = FundingSerializer(paginator, many=True)
            return response.JsonResponse(serializer.data, safe=False, status=200)
        else :
            isFriend = Follow.objects.filter(follower = user.id, followee = target_id).count() & Follow.objects.filter(follower = target_id, followee=user.id).count()
            fundings = Funding.objects.filter(author_id = target_id).order_by('-id') if isFriend else Funding.objects.filter(author_id = target_id, public=True).order_by('-id')
            paginator = paging_funding(request=request, list=fundings)
            serializer = FundingSerializer(paginator, many=True)
            return response.JsonResponse(serializer.data, safe=False, status=200)


class GetFollowFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET FOLLOW FUNDING')
    def get(self, request):

        user = Verify.jwt(self, request=request)

        #내가 팔로우한 사람들
        followee_users = Follow.objects.filter(follower=user.id).values_list('followee')
        #나를 팔로우한 사람들
        follower_users = Follow.objects.filter(followee=user.id).values_list('follower', flat=True)

        # 사용자가 팔로우한 사용자들의 펀딩 가져오기
        fundings = Funding.objects.filter(
            Q(author__in=followee_users) & (Q(public=True) |  # 내가 팔로우한 사람들의 공개 펀딩
            (Q(public=False)&Q(author__in=follower_users)))   # 비공개 펀딩 중 사용자가 작성자를 팔로우한 경우
        ).order_by('-created_on').select_related('author')
        paginator = manual_pagination(request=request,items=fundings,per_page=8)
        serializer = FundingSerializer(paginator, many=True)
        return response.JsonResponse(serializer.data, safe=False, status=200)
    

class GetJoinedFundings(APIView, JWTStatelessUserAuthentication):
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    @swagger_auto_schema(manual_parameters=[page], operation_description='GET JOINED FUNDING')
    def get(self, request):
        user = Verify.jwt(self, request=request)
        funding_ids = Remit.objects.filter(author_id = user.id).values('funding').distinct()
        fundings = Funding.objects.filter(id__in = funding_ids).order_by('-updated_on')
        fundings = Funding.objects.filter(id__in = funding_ids).order_by('-updated_on')
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
    



