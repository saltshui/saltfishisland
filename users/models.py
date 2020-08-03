from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    修改User模型，将用户名限定为邮箱，增加变量昵称
    '''
    nickname = models.CharField(
        '昵称',
        max_length=20,
        unique=True,
        error_messages={
            'unique': ("该昵称已被占用"),
        },)
    
    username = models.EmailField(
        '电子邮箱',
        max_length=150,
        unique=True,
        error_messages={
            'unique': ("该邮箱已被注册"),
        },
    )
    class Meta(AbstractUser.Meta):
        pass

