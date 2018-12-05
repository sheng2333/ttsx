from django.db import models
from df_user.base_model import baseModel
from tinymce.models import HTMLField
from df_user.models import *
# Create your models here.

class GoodsType(baseModel):
    name = models.CharField(max_length=50,verbose_name='商品种类名称')
    logo = models.CharField(max_length=20,verbose_name='标识')
    image = models.ImageField(upload_to='type',verbose_name='商品类型图片')

    class Meta:
        db_table='df_goods_type'
        verbose_name='商品种类'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name



class GoodsSKU(baseModel):
    status_choices=(
        (0,'下线'),
        (1,'上线'),
    )

    name = models.CharField(max_length=50,verbose_name='商品名称')
    type = models.ForeignKey('GoodsType',verbose_name='商品种类')
    goods = models.ForeignKey('Goods',verbose_name='商品SPU')
    desc = models.CharField(max_length=500,verbose_name='商品简介')
    price = models.DecimalField(max_digits=15,decimal_places=2,verbose_name='商品价格')
    unite = models.CharField(max_length=20,verbose_name='商品单位')
    image = models.ImageField(upload_to='goods',verbose_name='商品图片')
    stock = models.IntegerField(default=1,verbose_name='商品库存')
    sales = models.IntegerField(default=0,verbose_name='商品销量')
    status = models.SmallIntegerField(default=1,choices=status_choices,verbose_name='商品状态')


    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Goods(baseModel):

    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    detail = HTMLField(blank=True,verbose_name='商品详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(baseModel):
    sku = models.ForeignKey('GoodsSKU',verbose_name='商品')
    image = models.ImageField(upload_to='goods',verbose_name='图片路径')
    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name





class IndexGoodsBanner(baseModel):
    '''首页轮播商品展示模型类 轮播图'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexTypeGoodsBanner(baseModel):
    '''首页分类商品展示模型类  按商品类型展示模类型'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型')
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name
    def __str__(self):
        info=str(self.display_type) + self.sku.name
        return info


class IndexPromotionBanner(baseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class GoodSComment(baseModel):

    username = models.ForeignKey('df_user.User',verbose_name='用户')
    comments = models.CharField(max_length=300,verbose_name='评论内容')
    sku = models.ForeignKey('GoodsSKU',verbose_name='所属商品sku')
    parid = models.ForeignKey('self',null=True,verbose_name='评论对象')

    class Meta:
        db_table = 'df_goodsComment'
        verbose_name = "评论表"
        verbose_name_plural = verbose_name

    def __str__(self):
        info=self.username.username+':'+self.comments
        return info