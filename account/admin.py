from django.contrib import admin
from .models import Account
from django.utils.html import format_html

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'username', 'email', 'birthday', 'gender', 'age_range', 'is_active', 'image_tag')
    list_display_links = ('id',)

    search_fields = ['id']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return ''

    image_tag.short_description = 'Image'

    # 수정 폼에서 비밀번호 필드를 숨깁니다.
    fieldsets = (
        (None, {'fields': ('id', 'username', 'email')}),
        ('Personal info', {'fields': ('birthday', 'gender', 'age_range', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # 비밀번호 필드를 required=False로 변경합니다.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'username', 'email', 'birthday', 'gender', 'age_range', 'image', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Account, AccountAdmin)