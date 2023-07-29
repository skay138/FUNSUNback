from django.db import models
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

# Create your models here.

class Funding(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    #제목
    title = models.CharField(max_length=20, null=False)
    #내용
    content = models.TextField(max_length=255, null=False)
    #목표금액
    goal_amount = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(10000000)], null=False)
    #현재금액
    current_amount = models.IntegerField(default=0)
    #작성자
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Funding')
    #종료일
    expire_on = models.DateTimeField(auto_now_add=False, null=False, default=(timezone.now()+timedelta(days=30)))
    #작성날짜
    created_on = models.DateTimeField(auto_now_add=True)
    #수정날짜
    updated_on = models.DateTimeField(auto_now=True)
    #공개여부
    public = models.BooleanField(default=False)
    #이미지
    image = models.ImageField(
        upload_to='funding_image/',
        null=True
    )
    is_transmitted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}({self.author})"
    

