from django.contrib import admin
from .models import Funding
from django.utils.html import format_html
# Register your models here.


class FundingAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'content', 'author', 'goal_amount', 'current_amount','expire_on','is_transmitted','public','image_tag')
    list_display_links=('title',)
    list_filter = ['is_transmitted']
    search_fields = ['id','author__id']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if(obj.image):
            return format_html('<img src="{}"width="50" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'Image'




admin.site.register(Funding, FundingAdmin)