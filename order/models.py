from django.db import models
from df_user.models import *
# Create your models here.

from df_user.base_model import baseModel

class Payment(baseModel):
    payment_name=models.CharField(max_length=20,verbose_name='支付方式')
    payment_logo=models.CharField(max_length=20, verbose_name='支付方式LOGO')

    class Meta:
        db_table='df_order_payment'
        verbose_name='支付方式'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.payment_name


class OrderInfo(baseModel):
    PAY_METHOD_CHOICES = (
        (1,'货到付款'),
        (2,'微信支付'),
        (3,'支付宝'),
        (4,'银联支付')
    )
    ORDER_STATUS_CHOICES = (
        (1,'待支付'),
        (2,'待发货'),
        (3,'待收货'),
        (4,'待评价'),
        (5,'已完成')
    )
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name='订单id')
    user = models.ForeignKey('df_user.User',verbose_name='用户')
    addr = models.ForeignKey('df_user.UserInfo',verbose_name='地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES,default=3,verbose_name='支付方式')

    total_count = models.IntegerField(default=1,verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品总价')

    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='订单运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1,verbose_name='订单状态')
    trade_no = models.CharField(max_length=128,default='',verbose_name='支付编码')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.order_id

class OrderGoods(baseModel):
    order = models.ForeignKey('OrderInfo',verbose_name='订单')
    sku = models.ForeignKey('goods.GoodsSKU',verbose_name='商品sku')
    count = models.IntegerField(default=1,verbose_name='商品数目')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    is_comment = models.BooleanField(default=False,verbose_name='是否评价')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order
