from django.contrib import admin
from .models import Remit

# Register your models here.


class RemitAdmin(admin.ModelAdmin):
    
    list_display = ('id','funding','funding_id','author','author_id' ,'amount', 'message')
    list_display_links=('id',)

    search_fields = ['id','author__id']

admin.site.register(Remit, RemitAdmin)