from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.


class FunSunUserManager(UserManager):
    def create_user(self, userData, password=None):
        account = self.model(
            
        )
        for keys in userData:
            if hasattr(account, keys)== True:
                setattr(account, keys, userData[keys])
        account.save(using=self._db)
        return account



class Account(AbstractBaseUser):
    id = models.CharField(unique=True, primary_key=True, max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    ##custom
    birthday = models.CharField(max_length=4)
    nickname = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    age_range = models.CharField(max_length=5)


    class Meta:
        db_table = 'account'

    objects = FunSunUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['nickname']