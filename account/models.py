from typing import Any, Optional
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.utils.html import mark_safe
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
    
    def create_superuser(self, id:str, username: str, email: str | None, password: str | None, **extra_fields: Any) -> Any:
        account = self.model(
            id = id,
            username = username,
            email = self.normalize_email(email),
            password = make_password(password),
            created_on = datetime.now()
        )
        account.is_staff = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(unique=True, primary_key=True, max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    ##custom
    bank_account = models.CharField(max_length=30, null=True)
    birthday = models.CharField(max_length=4, null=True)
    username = models.CharField(max_length=20, db_index=True)
    gender = models.CharField(max_length=6, null=True)
    age_range = models.CharField(max_length=5, null=True)
    image = models.ImageField(
        upload_to='profile_image/',
        null=True
    )
    
    follower_count = models.IntegerField(default=0)
    followee_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'account'

    objects = FunSunUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'id']

    def __str__(self) -> str:
        return self.username


