from django.shortcuts import render

from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Remit, Account, Funding
# Create your views here.

from config.util import Verify, manual_pagination
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from django.utils import timezone



import json
import requests
import os

class RemitPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remit
        fields = ['funding', 'amount', 'message']

class RemitPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remit
        fields = ['id', 'message']

class RemitSerializer(serializers.ModelSerializer):

    def getAuthor(self, obj):
        image = obj.author.image.url if obj.author.image else None
        profile = {
            "id" : obj.author.id,
            "username" : obj.author.username,
            "image" : image
        }
        return profile
    
    
    author = serializers.SerializerMethodField('getAuthor')

    class Meta:
        model = Remit
        fields = ['id','message', 'author','created_on']


class RemitView(APIView, JWTStatelessUserAuthentication):
    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    page = openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1)
    #Funding id로 송금데이터 가져오기
    @swagger_auto_schema(manual_parameters=[id, page], operation_description='GET Remits INFO')
    def get(self, request):
        funding = Verify.funding(request=request)
        remits = funding.remit_funding.all().select_related('author')
        paging = manual_pagination(request=request, items=remits, per_page=8)
        serializer = RemitSerializer(paging, many=True)
        return response.JsonResponse(serializer.data,safe=False, status=200)

    #생성
    @swagger_auto_schema(operation_description='testing', request_body=RemitPostSerializer)
    def post(self, request):
        author = Verify.jwt(self, request=request)
        fundingObj = Funding.objects.get(id=request.data.get('funding'))
        amount = int(request.data.get('amount'))
        remit = Remit.objects.create(
            amount= amount,
            author=Account.objects.get(id=author.id),
            funding = fundingObj
        )
        
        for keys in request.data:
            if hasattr(remit, keys)== True:
                if(keys == 'amount'):
                    pass
                elif(keys == 'author'):
                    pass
                elif(keys == 'funding'):
                    pass
                else:
                    setattr(remit, keys, request.data[keys])
        remit.save()
        fundingObj.current_amount += amount
        fundingObj.updated_on = timezone.now()
        fundingObj.save()
        serializer = RemitSerializer(remit)
        return response.JsonResponse(serializer.data, status=201)

    @swagger_auto_schema(operation_description='testing', request_body=RemitPutSerializer)
    def put(self, request):
        author = Verify.jwt(request=request)
        remit = Verify.remit(request=request)
  
        if(remit.author.id == author.id):
            remit.message = request.data.get('message')
            remit.save()
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)
        
    #삭제
    @swagger_auto_schema(operation_description='testing', request_body=RemitPutSerializer)
    def delete(self, request):
        author = Verify.jwt(request=request)
        remit = Verify.remit(request=request)

        if(remit.author.id == author.id):
            remit.delete()
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)
        


class KakaoPay(APIView, JWTStatelessUserAuthentication):
    pg_token = openapi.Parameter('pg_token', openapi.IN_QUERY, type=openapi.TYPE_STRING, default=1234125)
    kakaoApiKey = 'ef1ad9b7217b279d7e7860cd9322e8b3'

    
    class serial(serializers.Serializer):
        tid = openapi.Parameter('tid', openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=["KAKAOPAY"], operation_description='ready', request_body=serial)
    def post(self, request):
        user = Verify.jwt(self, request=request)
        amount = request.data.get('amount')
        approvalUrl = f'http://projectsekai.kro.kr:5000/remit/kakaopay/ready'
        failUrl = f'http://projectsekai.kro.kr:5000/remit/kakaopay/fail'
        cancelUrl = f'http://projectsekai.kro.kr:5000/remit/kakaopay/cancel'

        headers = {
        'Authorization': f'KakaoAK {self.kakaoApiKey}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        }

        request_body = {
        'cid': 'TC0ONETIME',
        'partner_order_id': f'FUNSUN_KAKAOPAY{user.id}{timezone.now}',
        'partner_user_id': user.id,
        'item_name': 'FUNSUN_FUNDING',
        'quantity': 1,
        'total_amount': amount,
        'vat_amount': 0,
        'tax_free_amount': 0,
        'approval_url': approvalUrl,
        'fail_url': failUrl,
        'cancel_url': cancelUrl,
        }

        result = requests.post(url='https://kapi.kakao.com/v1/payment/ready', data=request_body, headers=headers).json()
        
        
        
        tid = result['tid']
        url = result['next_redirect_app_url']
        
        data = {
            "tid" : tid,
            "pg_token": None,
        }
        with open(f"media/remit_data/{user.id}.json", "w") as json_file:
            json.dump(data, json_file)

        return response.JsonResponse({'url':url},status=200)
    
    @swagger_auto_schema(tags=["KAKAOPAY"],manual_parameters=[pg_token], operation_description='kakaoPAY')
    def get(self, request):
        
        pg_token = request.GET.get('pg_token')

        # with open(f"media/remit_data/{pk}.json", "r") as json_file:
        #     data = json.load(json_file)

        # data["pg_token"]= pg_token

        # with open(f"media/remit_data/{pk}.json", "w") as json_file:
        #     json.dump(data, json_file)

        return response.HttpResponse(status=200)



class KakaoApproveView(APIView, JWTStatelessUserAuthentication):
    kakaoApiKey = 'ef1ad9b7217b279d7e7860cd9322e8b3'

    @swagger_auto_schema(tags=["KakaoApprove"], operation_description='test')
    def post(self, request):
        user = Verify.jwt(self, request=request)
        try : pg_token = request.data.get('pg_token')
        except:
            return response.HttpResponse(status=400)

        with open(f"media/remit_data/{user.id}.json", "r") as json_file:
            data = json.load(json_file)
        data['pg_token'] = pg_token

        with open(f"media/remit_data/{user.id}.json", "w") as json_file:
            json.dump(data, json_file)
        

        return response.HttpResponse(status=200)

    
    def get(self, request):
        user = user = Verify.jwt(self, request=request)

        with open(f"media/remit_data/{user.id}.json", "r") as json_file:
            data = json.load(json_file)

        requestBody = {
            'cid': 'TC0ONETIME',
            'tid': data['tid'],
            'item_name': 'FUNSUN_FUNDING',
            'partner_order_id':  f'FUNSUN_KAKAOPAY{user.id}{timezone.now}',
            'partner_user_id': user.id,
            
            'pg_token': data['pg_token'],
        }

        headers = {
        'Authorization': f'KakaoAK {self.kakaoApiKey}',
        }

        result = requests.post(url='https://kapi.kakao.com/v1/payment/approve', data=requestBody, headers=headers)
        print('최종작업')
        print(data)
        if(result.status_code == 200):
            os.remove(f"media/remit_data/{user.id}.json")
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)

   


