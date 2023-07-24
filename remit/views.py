from django.shortcuts import render
from django.shortcuts import render
from rest_framework import serializers
#Swagger
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 


from django.http import response
from .models import Remit
# Create your views here.

from config.util import Verify


class FundingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remit
        fields = '__all__'



class RemitView(APIView):
    #Funding id로 게시물 찾기
    def get(self, request):
        funding = Verify.funding(request=request)
        if(type(funding)==response.HttpResponse):
            return funding
        remits = Remit.objects.filter(funding=funding)
        serializer = FundingSerializer(remits, many=True)
        return response.JsonResponse(serializer.data, status=200)

    #생성
    def post(self, request):
        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author

        remit = Remit.objects.create(
            amount=int(request.data.get('amount')),
            author=author
        )
        
        for keys in request.data:
            if hasattr(remit, keys)== True:
                if(keys == 'amount'):
                    pass
                elif(keys == 'author'):
                    pass
                else:
                    setattr(remit, keys, request.data[keys])
        remit.save()
        serializer = FundingSerializer(remit)
        return response.JsonResponse(serializer.data, status=200)

    def put(self, request):
        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author
        remit = Verify.remit(request=request)
        if(type(remit)==response.HttpResponse):
            return remit

        if(remit.author == author):
            remit.message = request.data.get('message')
            remit.save()
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)
        
    #삭제
    def delete(self, request):

        author = Verify.author(request=request)
        if(type(author)==response.HttpResponse):
            return author
        remit = Verify.remit(request=request)
        if(type(remit)==response.HttpResponse):
            return remit

        if(remit.author == author):
            remit.delete()
            return response.HttpResponse(status=200)
        else:
            return response.HttpResponse(status=400)