from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin



class BaseUserManager(BUM):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email.lower()), username=username,is_admin=False)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password,is_admin=True)
        user.is_superuser = True
        user.save(using=self._db)
        return user
      

class BaseUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name = "email address",
                              unique=True)
    
    username = models.CharField(verbose_name = "username" , max_length = 255)
    is_admin = models.BooleanField(default=False,verbose_name="admin")

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username' ]

    def __str__(self):
        return self.email
    
    def is_staff(self):
        return self.is_admin
