from django.shortcuts import render,HttpResponse
from django.conf import settings
from goods.models import *
from order.models import *
from django.http import JsonResponse
import datetime
import time
import os
from alipay import AliPay

# Create your views here.

def handle(request):

    user=request.user


    # print(User.objects.get(id=))

    gids=request.POST.getlist('gids')



    userInfo=UserInfo.objects.filter(user_id=user.id,is_delate=0)

    for i in userInfo:
        ls=i.userAddr.split('-')

        sheng = ls[0]
        shi = ls[1]
        xian = ls[2]
        detail = ls[3]
        i.sheng=sheng
        i.shi=shi
        i.xian=xian
        i.detail=detail
        phone = i.userPhone[:3]+'****'+i.userPhone[7:]
        i.phone=phone

    conn = settings.REDIS_CONN
    cart_key = 'cart_%d' % user.id

    skuList = []
    toPrice = 0
    toCount = 0
    skuIdList=''
    for gid in gids:

        sku = GoodsSKU.objects.get(id=gid)
        count = conn.hget(cart_key,gid)
        print('count',count)
        amount = int(count)*sku.price
        sku.count = count
        sku.amount = amount
        skuList.append(sku)
        skuIdList+=gid+','

        toCount += int(count)
        toPrice += float(amount)

    # conn.hdel(cart_key, gid)

    print('skuIdList',skuIdList)
    skuIdList=skuIdList.strip(',')
    print('skuIdList',skuIdList)

    freight = 10

    payment=Payment.objects.filter(is_delate=0)

    allPrice=freight+toPrice
    context = {
        'userInfo':userInfo,
        'toCount': toCount,
        'toPrice': toPrice,
        'skuList': skuList,
        'freight': freight,
        'allPrice':allPrice,
        'payment':payment,
        'skuIdList':skuIdList
        }

    # conn.hdel(cart_key, sku_id)

    return render(request,'df_user/place_order.html',context)



def order_handle(request):
    time.sleep(5)
    skus=request.POST.get('skus')
    pay_style=request.POST.get('pay_style')
    addr_id=request.POST.get('addr')

    print(skus,pay_style,addr_id)

    user = request.user

    if not user.is_authenticated():
        print({'res': 0, 'errmsg': '用户未登录'})
        return JsonResponse({'res': 0, 'errmsg': '用户未登录'})


    # addr_id = request.POST.get('addr_id')
    # pay_method = request.POST.get('pay_method')
    # sku_ids = request.POST.get('sku_ids')
    # print(pay_method, addr_id,sku_ids)


    if not all([skus, pay_style, addr_id]):
        print({'res': 1, 'errmsg': '参数不完整'})
        return JsonResponse({'res': 1, 'errmsg': '参数不完整'})
    try:
        addr = UserInfo.objects.get(id=addr_id)
    except UserInfo.DoesNotExist:
        print({'res': 3, 'errmsg': '地址非法'})
        return JsonResponse({'res': 3, 'errmsg': '地址非法'})
    order_id = datetime.datetime.today().strftime('%Y%m%d%H%M%S') + str(user.id)
    print(order_id)


    transit_price = 10
    total_count = 0
    total_price = 0
    try:
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            addr=addr,
            pay_method=pay_style,
            total_price=total_price,
            total_count=total_count,
            transit_price=transit_price,
        )
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        sku_ids = skus.split(',')
        print('sku_ids',sku_ids)
        # sku_ids=sku_ids1[0,len(sku_ids1)-1]
        # print('sku_ids1',sku_ids1)


        for sku_id in sku_ids:
            print('sku_id',sku_id)
            try:
                sku = GoodsSKU.objects.get(id=sku_id)

            except:
                print({'res': 4, 'errsmg': '商品不存在'})
                return JsonResponse({'res': 4, 'errsmg': '商品不存在'})

            count = conn.hget(cart_key, sku_id)
            if int(count) > sku.stock:
                print({'res': 6, 'errmsg': '商品库存不足'})

                return JsonResponse({'res': 6, 'errmsg': '商品库存不足'})
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=count,
                price=sku.price
            )
            sku.stock -= int(count)
            sku.sales += int(count)
            sku.save()

            amount = sku.price * int(count)

            print('amountamountamount',amount)

            total_count += int(count)
            total_price += amount

            print('total_pricetotal_pricetotal_price',total_price)

        order.total_count = total_count
        order.total_price = total_price
        order.save()
    except Exception as e:
        print({'res': 7, 'errmsg': '下单失败'})

        return JsonResponse({'res': 7, 'errmsg': '下单失败'})
    conn.hdel(cart_key,sku_ids)
    print({'res':5,'errmsg':'订单提交成功'})

    return JsonResponse({'res':5,'errmsg':'订单提交成功'})



def OrderPay(request):
    # 用户是否登录
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'errmsg': '请先登录'})
    # 接收参数
    order_id = request.POST.get('order_id')
    print('111111')
    print('order_id', order_id)
    # 校验参数

    if not order_id:
        print('order_idqqqqq',order_id)
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        print('try')
        order = OrderInfo.objects.get(user=user,
                                      order_id=order_id,
                                      pay_method=3,
                                      order_status=1)
    except Exception as e:
        return JsonResponse({'res': 2, 'errmsg': '订单错误'})


    print('66666666666666666')
    # 业务初始化
    # 使用Python  sdk 调用支付宝接口

    alipay = AliPay(

        appid="2016092000551738",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, 'order/app_private_key.pem'),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, 'order/alipay_public_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False

    )
    print('777777777777777777')

    # 调用支付接口
    # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    total_pay = order.total_price + order.transit_price  # Decimal
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单id
        total_amount=str(total_pay),  # 支付总金额
        subject='ttsx%s' % order_id,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    print('order_string',order_string)
    # 返回应答
    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return JsonResponse({'res': 3, 'pay_url': pay_url})



def checkPay(request):
    '''查看订单支付结果'''

    # 用户是否登录
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res':0,'errmsg':'请先登录'})

    # 接收参数
    order_id = request.POST.get('order_id')

    #  校验参数
    if not order_id:
        return JsonResponse({'res':1,'errmsg':'无效的订单'})
    try:
        order = OrderInfo.objects.get(order_id=order_id,
                                      user=user,
                                      pay_method=3,
                                      order_status=1)
    except Exception as e:
        return JsonResponse({'res':2,'errmsg':'订单错误'})
    # 业务初始化:使用python sdk调用支付宝的支付接口
    # 初始化
    alipay = AliPay(
        appid="2016092000551738",  # 应用id
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, 'order/app_private_key.pem'),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, 'order/alipay_public_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False


    )
    # 调用支付宝的交易查询接口
    while True:
        response = alipay.api_alipay_trade_query(order_id)
        code = response.get('code')

        if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
            # 支付成功
            # 获取支付宝交易号
            trade_no = response.get('trade_no')
            # 更新订单状态
            order.trade_no = trade_no
            order.order_status = 4  # 待评价
            order.save()
            # 返回结果
            return JsonResponse({'res': 3, 'message': '支付成功'})
        elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
            # 等待买家付款
            # 业务处理失败，可能一会就会成功
            import time
            time.sleep(5)
            continue
        else:
            # 支付出错
            print(code)
            return JsonResponse({'res': 4, 'errmsg': '支付失败'})



def comment_all(request):

    # order_id=request.GET.get('order_id')



    user=request.user

    orderInfos=OrderInfo.objects.filter(user_id=user.id).order_by('-create_time')


    for i in orderInfos:

        goodsInfos=OrderGoods.objects.filter(order_id=i.order_id)

        i.goods=goodsInfos





    # return render(request, 'df_user/user_center_order.html', {'title': '天天生鲜-用户中心_订单', 'page': 2,'orderInfos':orderInfos})



    return render(request,'df_user/comment_all.html',{'title': '天天生鲜-用户中心_订单', 'page': 2,'orderInfos':orderInfos})


def comment_page(request):
    if request.method=='GET':
        order_id = request.GET.get('order_id')
        sku_id = request.GET.get('sku_id')
        # print(sku_id)

        order_info=OrderInfo.objects.get(order_id=order_id)
        sku=GoodsSKU.objects.get(id=sku_id)
        # print(sku.name)
        return render(request,'df_user/comment_page.html',{'sku':sku,'order_info':order_info})


    elif request.method=='POST':



        sku_id = request.POST.get('sku_id')
        message = request.POST.get('message')
        user = request.user

        # if OrderGoods.objects.get(order_id=order_id, user_id=user.id):
        #     sku_info = OrderGoods.objects.get(order_id=order_id, sku_id=sku_id)
        #
        #     GoodSComment.objects.get()



        GoodSComment.objects.create(username_id=user.id, comments=message, sku_id=sku_id)

        goods=OrderGoods.objects.get(sku_id=sku_id)

        goods.is_comment=True




        return HttpResponse('评论成功')




# def comment_page_handle(request):
#     order_id=request.GET.get('order_id')
#     sku_id=request.GET.get('sku_id')
#
#     user = request.user
#
#
#     if OrderGoods.objects.get(order_id=order_id,user_id=user.id):
#         sku_info=OrderGoods.objects.get(order_id=order_id,sku_id=sku_id)
#
#         GoodSComment.objects.get()
#
#
#
#     return render(request,'df_user/comment_page.html')