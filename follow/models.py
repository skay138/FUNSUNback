from django.db import models
from account.models import Account

# Create your models here.

# 팔로워 / 팔로우 중개 모델
class Follow(models.Model):
    #나를 팔로우 하는 사람들
    follower = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='follower'
        )
    #내가 팔로우 하는 사람들
    followee = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='followee'
        )

    def following(self):
        return f'{self.follower.id} is following {self.followee.id}'