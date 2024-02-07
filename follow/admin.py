from django.contrib import admin
from .models import Follow

# Register your models here.
class FollowAdmin(admin.ModelAdmin):
    
    list_display = ('id','follower','followee')
    list_display_links=('id',)

    search_fields = ['id','follower','followee']

admin.site.register(Follow, FollowAdmin)