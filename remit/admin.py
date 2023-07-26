from django.contrib import admin
from .models import Remit

# Register your models here.


class RemitAdmin(admin.ModelAdmin):
    
    list_display = ('id','funding','author', 'amount', 'message')
    list_display_links=('id',)

    search_fields = ['id','author__id']

admin.site.register(Remit, RemitAdmin)