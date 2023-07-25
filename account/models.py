from typing import Any, Optional
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from datetime import datetime
from django.contrib.auth.hashers import make_password
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
    birthday = models.CharField(max_length=4)
    username = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    age_range = models.CharField(max_length=5)


    class Meta:
        db_table = 'account'

    objects = FunSunUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'id']

    def getuserid(self):
        return self.id


