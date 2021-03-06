from django.shortcuts import render
import time
# Create your views here.


from django.shortcuts import render

from django.shortcuts import render
from cart.models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from goods.models import *


def add(request):
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')

    if not all([sku_id, count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        count = int(count)
    except Exception as e:
        return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
    try:
        sku = GoodsSKU.objects.get(id=sku_id)
    except GoodsSKU.DoesNotExist:
        return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
    conn = settings.REDIS_CONN
    cart_key = 'cart_%d' % user.id
    cart_count = conn.hget(cart_key, sku_id)
    if cart_count:
        count += int(cart_count)
    if count > sku.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
    conn.hset(cart_key, sku_id, count)
    total_count = get_cart_count(user)
    return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


def get_cart_count(user):
    total_count = 0
    if user.is_authenticated():
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        cart_dict = conn.hgetall(cart_key)
        for sku_id, count in cart_dict.items():
            total_count += int(count)
    return total_count


def cart_cen(request):
    user = request.user
    conn = settings.REDIS_CONN
    cart_key = 'cart_%d' % user.id
    cart_dict = conn.hgetall(cart_key)

    skuList = []
    toPrice = 0
    toCount = 0

    for k, v in cart_dict.items():
        skuInfo = GoodsSKU.objects.get(id=k)

        skuInfo.count = int(v)
        print('skuInfo.price',skuInfo.price)
        skuInfo.sPrice = (skuInfo.price)*10000/10000 * int(skuInfo.count)


        print('skuInfo.sPrice',skuInfo.sPrice)
        skuList.append(skuInfo)

        # cart_count = conn.hget(cart_key, )

        toPrice += skuInfo.sPrice
        toCount += skuInfo.count

    if len(skuList) != 0:
        is_null = 1
    else:
        is_null = 0
    context = {
        'toCount': toCount,
        'toPrice': toPrice,
        'skuList': skuList,
        'is_null': is_null
    }
    return render(request, 'df_user/cart.html', context)


def cart_update(request):
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')

    if not all([sku_id, count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        print('qqqqqq')
        print(count)
        count = int(count)

    except Exception as e:
        return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
    try:
        sku = GoodsSKU.objects.get(id=sku_id)
    except GoodsSKU.DoesNotExist:
        return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
    conn = settings.REDIS_CONN
    cart_key = 'cart_%d' % user.id

    if count > sku.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
    conn.hset(cart_key, sku_id, count)
    total_count = get_cart_count(user)

    return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


def cart_delete(request):
    user = request.user
    sku_id = request.POST.get('sku_id')
    if not sku_id:
        return JsonResponse({'res': 1, 'errmsg': '无效的商品id'})
    try:
        sku = GoodsSKU.objects.get(id=sku_id)
    except GoodsSKU.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '商品不存在'})
    conn = settings.REDIS_CONN
    cart_key = 'cart_%d' % user.id
    conn.hdel(cart_key, sku_id)
    total_count = get_cart_count(user)
    return JsonResponse({'res': 3, 'total_count': total_count, 'message': '删除成功'})


def show_cart_count(request):
    user = request.user
    cart_count = get_cart_count(user)
    return JsonResponse({"cart_count": cart_count})
