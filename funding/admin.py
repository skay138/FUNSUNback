from django.contrib import admin
from .models import Funding

# Register your models here.


class FundingAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'title', 'content', 'author', 'goal_amount', 'public',)
    list_display_links=('title',)


admin.site.register(Funding, FundingAdmin)