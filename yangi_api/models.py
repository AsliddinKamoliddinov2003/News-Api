from django.db import models
from django.db.models.fields import CharField, TextField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or not password:
            raise Exception
        
        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True, null=True)
    is_staff = models.BooleanField(default=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    is_seperuser = models.BooleanField(default=False, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

