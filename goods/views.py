from django.shortcuts import render,redirect
from .models import *
import random
from redis import *
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    # print(request.user)

    # 查询全部商品分类
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
    context = {
        'types': types,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners,
        'title': '天天生鲜-首页', 'guest_cart': 1,
               }
    return render(request, 'df_user/h1.html', context)



    # GoodsTypeList=GoodsType.objects.filter(is_delate=0)
    # # GoodsSPUList=Goods.objects.filter(is_delate=0)
    # GoodsSKUList=GoodsSKU.objects.filter(status=1,is_delate=0)
    #
    #
    #
    # # skuList=[]
    # # for a in GoodsSKUList:
    # #     if len(skuList)<4 and a.goods not in skuList:
    # #
    # #         skuList.append(a)
    # #
    # #
    # # print('skuList',skuList)
    #
    #
    # # print('GoodsSPUList',GoodsSPUList)
    # # print('GoodsSKUList',GoodsSKUList)
    #
    # typeList=[]
    # for i in GoodsTypeList:
    #     if i not in typeList and len(typeList)<=6:
    #         typeList.append(i)
    #
    # print('typeList',typeList)
    #
    # GoodsList = []
    # GoodsLists=[]
    # for j in typeList:
    #     goods=GoodsSKUList.filter(type_id=j.id)
    #     if len(GoodsList)<6:
    #         print('goods',goods)
    #         for k in goods:
    #             if len(GoodsLists) < 4:
    #                 GoodsLists.append(k)
    #             print('GoodsLists',GoodsLists)
    #
    #         for l in GoodsLists:
    #             GoodsList.append(l)
    #         GoodsLists = []
    # #
    # # print('GoodsList',GoodsList)
    #
    # return render(request, 'df_user/indexes.html',{'GoodsTypeList':typeList,'skuList':GoodsList})

def detail(request):
    # gid=request.GET.get('id')
    skuid=request.GET.get('skuid')
    urls_get = request.get_full_path()

    userInfo=request.user

    if not userInfo.is_authenticated():
        userInfo=''


    # comment=GoodSComment.objects.filter(sku_id=skuid,parid_id__isnull=True)
    comment=GoodSComment.objects.filter(sku_id=skuid,parid_id__isnull=True)

    for com in comment:
        print(com.id)
        com.com2 = GoodSComment.objects.filter(sku_id=skuid, parid_id=com.id)

    print(comment)



    comment2=GoodSComment.objects.filter(sku_id=skuid,parid_id__isnull=False)

    GoodsSKUInfo=GoodsSKU.objects.get(id=skuid,is_delate=0)
    typeid=GoodsSKU.objects.get(id=skuid,is_delate=0).type_id
    GoodInfo=GoodsSKU.objects.filter(is_delate=0,type_id=typeid)


    type_list=GoodsSKU.objects.filter(goods_id=GoodsSKU.objects.get(id=skuid,is_delate=0).goods_id)


    goodsNewList=[]
    i=0
    while i < 2:
        random_num=random.randint(0,len(GoodInfo)-1)

        if GoodInfo[random_num] not in goodsNewList:
            goodsNewList.append(GoodInfo[random_num])
            i+=1
    Goods_image=GoodsImage.objects.filter(sku_id=skuid)

    user = request.user
    if user.is_authenticated():

        con=StrictRedis('192.168.12.181')

        history_key='history_%d'%user.id

        con.lrem(history_key,0,GoodsSKUInfo.id)

        con.lpush(history_key,GoodsSKUInfo.id)

        # print(history_key)

        # con.ltrim(history_key,0,4)

    # GoodsInfo=Goods.objects.get(id=skuid,is_delate=0)
    # sku_info=GoodsImage.objects.get(sku_id=skuid,is_delate=0)
    return render(request, 'df_user/detail.html',{'comment':comment,'comment2':comment2,'userInfo':userInfo,'GoodsImage':Goods_image,'GoodsSKUInfo':GoodsSKUInfo,'goodsNew':goodsNewList,'skus':type_list,'urls':urls_get})

def goodsList(request):
    gid=request.GET.get('type')
    orderBy=request.GET.get('order_by')
    pageInfo=request.GET.get('page')




    GoodsList=GoodsSKU.objects.filter(type_id=gid,is_delate=0,status=1)

    goodsType=GoodsType.objects.get(id=GoodsList[0].type_id)
    if orderBy == None:
        orderBy = 'default'

    if pageInfo == None:
        pageInfo = 1
    else:
        pageInfo=int(pageInfo)

    if orderBy=='price':
        GoodsList=GoodsList.order_by('price')
        num='2'
    elif orderBy=='pop':
        GoodsList=GoodsList.order_by('sales')
        num='3'
    else:
        GoodsList=GoodsList.order_by('-id')
        num='1'
    goodsNewList = []
    i = 0
    while i < 2:
        random_num = random.randint(0, len(GoodsList) - 1)

        if GoodsList[random_num] not in goodsNewList:
            goodsNewList.append(GoodsList[random_num])
            i += 1


    my_pagenator = Paginator(GoodsList, 2)
    pages = my_pagenator.page(int(pageInfo))
    # page_n=pages.paginator.page_range

    num_page=my_pagenator.num_pages


    if num_page<5:
        page_n=range(1,num_page+1)
    elif pageInfo<=3:
        page_n=range(1,6)
    elif num_page-pageInfo<=2:
        page_n=range(num_page-4,num_page+1)
    else:
        page_n=range(pageInfo-2,pageInfo+3)


    context={'typeId':gid,'goodsType':goodsType,'num':num,'goodsNew':goodsNewList,'pages':pages,'orderBy':orderBy,'page_n':page_n}

    return render(request, 'df_user/list.html',context)



# def get(self, request):
#     # 查询全部商品分类
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
#     context = {'types': types,
#                'goods_banners': goods_banners,
#                'promotion_banners': promotion_banners,
#                'title': '天天生鲜-首页', 'guest_cart': 1,
#                }
#     return render(request, 'df_goods/indexes.html', context)


def comment(request):
    user_get=request.POST.get('user')
    goods_get=request.POST.get('goods')
    obj_get=request.POST.get('obj')
    comment_get=request.POST.get('comment')
    urls_get=request.POST.get('urls')


    # print('user_get',user_get)
    # print('goods_get',goods_get)
    # print('obj_get',obj_get)
    # print('comment_get',comment_get)
    # print('urls',urls_get)

    GoodSComment.objects.create(username_id=user_get, comments=comment_get, sku_id=goods_get, parid_id=obj_get)

    return redirect(urls_get)


import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator

# from django.views import View
from django.views.generic.base import View

class Comment2(View):
    def get(self):
        return HttpResponse('ok')