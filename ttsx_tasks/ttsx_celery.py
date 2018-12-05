# # from celery import Celery
# # from django.core.mail import send_mail
# # import os
# # import django
# # # from goods.models import *
# # from django.template import loader
# # from django.conf import settings
# #
# #
# # app = Celery('ttsx_tasks.ttsx_celery', broker='redis://192.168.12.181:6379/3')
# #
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ttsx.settings")
# # django.setup()
# #
# # from goods.models import GoodsType,IndexGoodsBanner,IndexTypeGoodsBanner,IndexPromotionBanner
#
#
#
# from celery import Celery
# from django.core.mail import send_mail
# from goods.models import *
# from df_user.models import *
# from django.template import loader
# from django .conf import settings
#
# # 为celery配置django环境
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()
#
# app = Celery('ttsx_tasks.ttsx_celery', broker='redis://192.168.12.181:6379/3')
#
#
#
# @app.task
# def celery_send_mail(send_title, send_message, EMAIL_FROM, send_obj_list,send_html_message):
#     print('0')
#     send_statue=send_mail(send_title, send_message, EMAIL_FROM, send_obj_list, html_message=send_html_message)
#     print(send_statue)
#
# # @app.task
# # def task_generate_static_index():
# #     print('静态首页开始生成。。。')
# #
# #     types = GoodsType.objects.all()
# #     goods_banners = IndexGoodsBanner.objects.all().order_by('indexes')  # 获得轮播图片
# #     promotion_banners = IndexPromotionBanner.objects.all().order_by('indexes')  # 获取活动图片
# #     print('11111')
# #     for type in types:
# #         # 获取type种类首页分类商品的图片展示信息
# #         image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1, ).order_by('indexes')
# #         title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0, ).order_by('indexes')
# #         # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
# #         type.image_banners = image_banners
# #         type.title_banners = title_banners
# #     print('22222')
# #
# #     context = {
# #         'types': types,
# #         'goods_banners': goods_banners,
# #         'promotion_banners': promotion_banners,
# #         'title': '天天生鲜-首页', 'guest_cart': 1,
# #     }
# #     print(context)
# #     print('33333')
# #
# #     temp=loader.get_template('df_user/h11.html')
# #     print('33333-1')
# #
# #     static_index_html=temp.render(context)
# #     print('33333-2')
# #
# #     save_path=os.path.join(settings.BASE_DIR,'static/html/indexes.html')
# #     print('44444')
# #
# #     with open(save_path,'w') as fl:
# #         fl.write(static_index_html)
# #
# #
# #     print('静态首页生成结束。。。')
#
#     @app.task
#     def task_generate_static_index():
#         '''产生首页静态页面'''
#
#         print('生成静态首页begin...')
#
#         types = GoodsType.objects.all()
#         goods_banners = IndexGoodsBanner.objects.all().order_by('indexes')  # 获得轮播图片
#         promotion_banners = IndexPromotionBanner.objects.all().order_by('indexes')  # 获取活动图片
#         for type in types:
#             # 获取type种类首页分类商品的图片展示信息
#             image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1, ).order_by('indexes')
#             title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0, ).order_by('indexes')
#             # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
#             type.image_banners = image_banners
#             type.title_banners = title_banners
#
#         # 获取用户购物车中的商品数量，待完善
#         cart_count = 0
#
#         # 准备数据字典
#         context = {'types': types,
#                    'goods_banners': goods_banners,
#                    'promotion_banners': promotion_banners,
#                    'cart_count': cart_count,
#                    'title': '天天生鲜-首页', 'guest_cart': 1,
#                    }
#
#         # 使用模板
#         # 1、加载模板文件，返回模板对象
#         temp = loader.get_template('df_user/h11.html')
#         # 2、模板渲染
#         static_index_html = temp.render(context)
#
#         # 生成首页对应静态文件
#         save_path = os.path.join(settings.BASE_DIR, 'static/html/indexes.html')
#         with open(save_path, 'w') as f:
#             f.write(static_index_html)
#
#         print('生成静态首页end...')




# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()
#
#
# from celery import Celery
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template import loader
#
#
# from df_goods.models import *
# app=Celery('celery_task.tasks',broker='redis://192.168.12.186:6379/3')
#
#
# @app.task
# def send_email_task(subject, message, sender, receiver, html_message):
#     print('celery...begin')
#     send_mail(subject, message, sender, receiver, html_message=html_message)
#     print('celery...end')
#
# @app.task
# def task_generate_static_index():
#     '''产生首页静态页面'''
#
#     # 查询全部商品分类
#     print('开始。。。')
#     types = GoodsType.objects.all()
#     goods_banners = IndexGoodsBanner.objects.all().order_by('indexes')  # 获得轮播图片
#     promotion_banners = IndexPromotionBanner.objects.all().order_by('indexes')  # 获取活动图片
#     for type in types:
#         # 获取type种类首页分类商品的图片展示信息
#         image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1, ).order_by('indexes')
#         title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0, ).order_by('indexes')
#         # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
#         type.image_banners = image_banners
#         type.title_banners = title_banners
#
#     #组织模板上下文
#     context = {'types': types,
#                'goods_banners': goods_banners,
#                'promotion_banners': promotion_banners,
#                'title': '天天生鲜-首页', 'guest_cart': 1,
#                }
#     #使用模板
#     #1.加载模板文件，返回模板对象
#     temp=loader.get_template('df_goods/sindex.html')
#
#     #2。模板渲染
#     static_index_html=temp.render(context)
#
#     #生成首页对应静态文件
#     save_path=os.path.join(settings.BASE_DIR,'static/html/indexes.html')
#     with open(save_path,'w') as f:
#         f.write(static_index_html)
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ttsx.settings")
django.setup()

from celery import Celery
from django.core.mail import send_mail
from goods.models import *
from django.template import loader
from django .conf import settings

# 为celery配置django环境

app=Celery('ttsx_tasks.ttsx_celery',broker='redis://192.168.12.181:6379/3')


# celery -A ttsx_tasks.ttsx_celery worker -l info





@app.task
def celery_send_mail(send_title, send_message, EMAIL_FROM, send_obj_list,send_html_message):
    print('0')
    send_statue=send_mail(send_title, send_message, EMAIL_FROM, send_obj_list, html_message=send_html_message)
    print(send_statue)



@app.task
def task_generate_static_index():
    '''产生首页静态页面'''

    print('生成静态首页egin...')

    types = GoodsType.objects.all()
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')  # 获得轮播图片
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')  # 获取活动图片
    for type in types:
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1, ).order_by('index')
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0, ).order_by('index')
        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 获取用户购物车中的商品数量，待完善
    cart_count = 0

    # 准备数据字典
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners,
               'cart_count': cart_count,
               'title': '天天生鲜-首页', 'guest_cart': 1,
               }

    #使用模板
    #1、加载模板文件，返回模板对象
    temp=loader.get_template('df_user/h11.html')
    #2、模板渲染
    static_index_html=temp.render(context)

    #生成首页对应静态文件
    save_path=os.path.join(settings.BASE_DIR,'static/html/indexes.html')
    with open(save_path,'w') as f:
        f.write(static_index_html)

    print('生成静态首页end...')













