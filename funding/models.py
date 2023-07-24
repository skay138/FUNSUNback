from django.db import models
from account.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Funding(models.Model):
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
    #작성날짜
    created_on = models.DateTimeField(auto_now_add=True)
    #수정날짜
    updated_on = models.DateTimeField(auto_now=True)
    #공개여부
    public = models.BooleanField(default=False)
    #이미지
    img = models.TextField()
    

