from django.db import models
from account.models import Account

# Create your models here.


class Report(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    type = models.CharField(max_length=10)
    target = models.CharField(max_length=20)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Report')
    message = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)