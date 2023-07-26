from django.contrib import admin
from .models import Account
from django.utils.html import format_html

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'username', 'email', 'birthday', 'gender', 'age_range','is_active','image_tag')
    list_display_links=('id',)

    search_fields = ['id']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if(obj.image):
            return format_html('<img src="{}"width="50" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'Image'



admin.site.register(Account, AccountAdmin)