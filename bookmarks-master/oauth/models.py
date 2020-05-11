from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OAuthQQ(models.Model):
    """QQ and User Bind"""
    user = models.ForeignKey(User)   # 关联用户信息表
    qq_openid = models.CharField(max_length=64)   # QQ的关联OpenID

