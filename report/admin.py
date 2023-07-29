from django.contrib import admin
from .models import Report

# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    
    list_display = ('id','type','target', 'author', 'message','is_solved')
    list_filter = ['is_solved']
    list_display_links=('id',)

admin.site.register(Report, ReportAdmin)