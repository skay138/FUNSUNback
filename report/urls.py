from django.contrib import admin
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.ReportView.as_view())
]
