from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi 

from .models import Report, Account

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from config.util import Verify
from django.http import response
# Create your views here.

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

class ReportPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['type', 'target', 'message']

class ReportView(APIView, JWTStatelessUserAuthentication):

    @swagger_auto_schema(request_body=ReportPostSerializer)
    def post(self, request):
        author = Verify.jwt(self, request=request)
        report = Report.objects.create(
            author= Account.objects.get(id=author.id)
        )

        for keys in request.data:
            if hasattr(report, keys) == True:
                if (keys == 'author'):
                    pass
                else:
                    setattr(report, keys, request.data[keys])
        report.save()
        serializer = ReportSerializer(report)

        return response.JsonResponse(serializer.data, status=201)