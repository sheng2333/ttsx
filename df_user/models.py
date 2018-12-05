from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from .base_model import baseModel


class User(AbstractUser,baseModel):

    class Meta:
        db_table='df_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name

class UserInfo(baseModel):
    userShou=models.CharField(max_length=20,default='',verbose_name='收件人')
    userAddr=models.CharField(max_length=100,default='',verbose_name='收货地址')
    userYoubian=models.CharField(max_length=6,default='',verbose_name='邮编')
    userPhone=models.CharField(max_length=11,default='',verbose_name='手机')
    isShow=models.BooleanField(default=False,verbose_name='默认地址')
    user=models.ForeignKey(User)

    class Meta:
        db_table = 'df_userinfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name





class AreaInfo(models.Model):
    title = models.CharField(max_length=50)
    parea = models.ForeignKey('self', null=True)

# class TArea(models.Model):
#     areaid = models.AutoField(db_column='areaId', primary_key=True)  # Field name made lowercase.
#     areacode = models.CharField(db_column='areaCode', max_length=50)  # Field name made lowercase.
#     areaname = models.CharField(db_column='areaName', max_length=20)  # Field name made lowercase.
#     level = models.IntegerField(blank=True, null=True)
#     citycode = models.CharField(db_column='cityCode', max_length=50, blank=True,
#                                 null=True)  # Field name made lowercase.
#     center = models.CharField(max_length=50, blank=True, null=True)
#     parentid = models.IntegerField(db_column='parentId', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'T_Area'
