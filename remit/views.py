from django.shortcuts import render

from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Remit, Account, Funding
# Create your views here.

from config.util import Verify, paging_remit
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

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
        id = obj.author.id
        author = Account.objects.get(id = id)
        profile = {
            "id" : author.id,
            "username" : author.username,
            "image" : author.image.url
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
        remits = Remit.objects.filter(funding=funding)
        paging = paging_remit(request=request, list=remits)
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
        fundingObj.save()
        serializer = RemitSerializer(remit)
        return response.JsonResponse(serializer.data, status=200)

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