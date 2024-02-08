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

#redis
import redis
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.conf import settings

class PublicFundingsCache():
    update_interval = settings.REDIS_CACHE.get('UPDATE_INTERVAL', 5)
    expiration_time = settings.REDIS_CACHE.get('EXPIRATION_TIME', 24 * 60 * 60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get_cached_data(self):
            cached_data = self.redis_client.get('cached_data')
            if cached_data:
                return json.loads(cached_data)
            return None
    
    def update_cached_data(self):
        cached_time_str = self.redis_client.get('public_punding_cached_time')
        if cached_time_str:
            cached_time = datetime.fromisoformat(cached_time_str.decode())
            if datetime.now() - cached_time > timedelta(seconds=self.update_interval):
                self._update_cached_data()
        else:
            # 'public_punding_cached_time' 키에 해당하는 값이 없는 경우 새로운 값을 설정
            self._update_cached_data()

    def _update_cached_data(self):
        fundings = Funding.objects.filter(public=True).order_by('-id').select_related('author')
        serializer = FundingSerializer(fundings, many=True)
        data = serializer.data
        self.redis_client.set('cached_data', json.dumps(data, cls=DjangoJSONEncoder), ex=self.expiration_time)
        self.redis_client.set('public_punding_cached_time', datetime.now().isoformat())
        print("캐싱 완료")


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
            if public == True:
                cache = PublicFundingsCache()
                cache.update_cached_data()
            serializer = FundingDetailSerializer(funding)
            return response.JsonResponse(serializer.data, status=201)
        
    
    @swagger_auto_schema(operation_description='testing', request_body=FundingPutSerializer)
    def put(self, request):
        author = Verify.jwt(self, request=request)
        funding = Verify.funding(request=request)
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
            if public == True:
                cache = PublicFundingsCache()
                cache.update_cached_data()
                
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
        public_fundings_cache = PublicFundingsCache()  # PublicFundingsCache 클래스의 인스턴스 생성
        cached_data = public_fundings_cache.get_cached_data()  # 인스턴스 메서드 호출
        if cached_data is None:
            public_fundings_cache.update_cached_data()  # 인스턴스 메서드 호출
            cached_data = public_fundings_cache.get_cached_data()  # 인스턴스 메서드 호출
        paginator = manual_pagination(request=request,items=cached_data,per_page=8)
        return response.JsonResponse(paginator, safe=False, status=200)
    
    def post(self, req):
        return response.JsonResponse({"post":"요청댐"})
    



