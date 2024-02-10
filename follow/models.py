from django.db import models
from account.models import Account

# Create your models here.

# 팔로워 / 팔로우 중개 모델
class Follow(models.Model):
    #나를 팔로우 하는 사람들
    follower = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='follower_account'
        )
    #내가 팔로우 하는 사람들
    followee = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='followee_account'
        )

    def following(self):
        return f'{self.follower.id} is following {self.followee.id}'
    
    def save(self, *args, **kwargs):
        # 새로운 팔로우가 생성되었을 때
        if not self.pk:
            self.follower.follower_count += 1
            self.follower.save()
            self.followee.followee_count += 1
            self.followee.save()
            super().save(*args, **kwargs)
             
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.follower.followee_count = Follow.objects.filter(follower = self.follower.id).count()
        self.follower.follower_count = Follow.objects.filter(followee = self.follower.id).count()
        self.follower.save()
        self.followee.follower_count = Follow.objects.filter(followee = self.followee.id).count()
        self.followee.followee_count = Follow.objects.filter(follower = self.followee.id).count()
        self.followee.save()