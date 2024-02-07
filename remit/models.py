from django.db import models
from account.models import Account
from funding.models import Funding

# Create your models here.

class Remit(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    #작성자
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='remit_author')
    #펀딩
    funding = models.ForeignKey(Funding, on_delete=models.CASCADE, related_name='remit_funding')
    #금액
    amount = models.IntegerField()
    #작성날짜
    created_on = models.DateTimeField(auto_now_add=True)
    #메세지
    message = models.TextField(null=True)