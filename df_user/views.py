from django.shortcuts import render, redirect
import hashlib
from .models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random
import re
from itsdangerous import TimedJSONWebSignatureSerializer as tms, SignatureExpired, BadSignature
from django.conf import settings
# from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from ttsx_tasks.ttsx_celery import celery_send_mail
from django.contrib.auth.decorators import login_required
from goods.models import *
from redis import *
from order.models import *

def encrypt_sha1(info):
    m = hashlib.sha1()
    m.update(bytes(info, encoding='utf-8'))
    return m.hexdigest()


# Create your views here.


def register(request):
    return render(request, 'df_user/register.html', {'title': '天天生鲜-注册'})


def register_handle(request):
    userName = request.POST.get('user_name')
    userPwd1 = request.POST.get('pwd')
    userPwd2 = request.POST.get('cpwd')
    userEmail = request.POST.get('email')
    # register_url = reverse('user:register')
    # login_url = reverse('user:login')
    register_jump_url = reverse('user:register_jump')
    if not all([userName, userPwd1, userPwd2, userEmail]):
        return render(request, 'df_user/register.html', {'error': '信息不完整'})
    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', userEmail):
        return render(request, 'df_user/register.html', {'error': '邮箱格式错误'})

    user = User.objects.create_user(userName, userEmail, userPwd1)
    user.is_active = 0
    user.save()

    info = tms(settings.SECRET_KEY, 3600)
    token = info.dumps({'id': user.id}).decode()
    active_url = 'http://192.168.12.181:8000/user/active?url=' + token

    send_title = '天天生鲜-邮箱激活'
    send_message = ''
    send_obj_list = [userEmail]  # 收件人列表
    send_html_message = '<h1>欢迎用户%s,点击链接即可激活</h1> <a href="%s">激活</a>' % (userName,active_url)
    # send_statue=send_mail(send_title, send_message, settings.EMAIL_FROM, send_obj_list, html_message=send_html_message)

    celery_send_mail.delay(send_title, send_message, settings.EMAIL_FROM, send_obj_list, send_html_message)
    # 发送状态,可用可不用
    # print(send_statue)

    return redirect(register_jump_url)


def userName_exit(request):
    userName = request.GET.get('uname')
    return JsonResponse({'count': (User.objects.filter(username=userName).count())})


def email_exit(request):
    email = request.GET.get('email')
    # print((User.objects.filter(userEmail=email).count()))
    return JsonResponse({'count': (User.objects.filter(userEmail=email).count())})


def check_yzm(request):
    yzm = request.GET.get('yzm')
    if yzm.lower() == request.session['yanzhengma']:
        return JsonResponse({'count': 0})
    else:
        return JsonResponse({'count': 1})


def loginCheck(request):
    userName = request.GET.get('username')
    userPwd = request.GET.get('pwd')
    user_center_info_url = reverse('user:user_center_info')
    count = User.objects.filter(userName=userName, userPwd=userPwd).count()
    if count != 1:
        return JsonResponse({'count': count})
    else:
        return redirect(user_center_info_url)


# def login(request):


def user_login(request):
    if request.method == 'POST':
        userName = request.POST.get('username')
        userPwd = (request.POST.get('pwd'))
        remember = request.POST.get('remember', '')
        register_url = reverse('user:register')
        index_url = reverse('goods:index')
        next_url = request.GET.get('next')


        user = authenticate(username=userName, password=userPwd)
        if user is not None:
            if next_url:
                resp = redirect(next_url)
            else:
                resp = redirect(index_url)
            if remember == 'on':
                resp.set_cookie('user_name_c', userName)
            else:
                resp.set_cookie('user_name_c', '')

            if user.is_active:
                login(request, user)

            else:
                return render(request, 'df_user/login.html',
                              {'title': '天天生鲜-登录', 'login_error': 2, 'user_name_c': userName})
            return resp

        else:
            return render(request, 'df_user/login.html',
                          {'title': '天天生鲜-登录', 'login_error': 1, 'user_name_c': userName})


    elif request.method == 'GET':
        logout(request)
        userName = request.COOKIES.get('user_name_c', '')
        return render(request, 'df_user/login.html', {'title': '天天生鲜-登录', 'user_name_c': userName})


def user_logout(request):
    logout(request)
    index_url = reverse('goods:index')
    return redirect(index_url)


# @login_required(login_url='/user/login')
@login_required
def user_center_info(request):
    user_id = request.session.get('_auth_user_id')

    if user_id != None:
        user = User.objects.filter(id=user_id)[0]
        userName = user.username

        con = StrictRedis('192.168.12.181')
        history=con.lrange('history_%d'%user.id,0,-1)

        his_list=[]
        for i in history:
            if len(his_list)<5:
                his_sku = GoodsSKU.objects.get(id=i)
                his_list.append(his_sku)

        print(his_list)

        if len(UserInfo.objects.filter(user_id=user_id,isShow=True,is_delate=False)) > 0:
            user_info = UserInfo.objects.filter(user_id=user_id,isShow=True,is_delate=False)[0]
            userPhone = user_info.userPhone
            userAddr = user_info.userAddr

            context = {'title': '天天生鲜-用户中心', 'userName': userName, 'userPhone': userPhone, 'userAddr': userAddr,
                       'page': 1,'his_list':his_list}
        else:
            context = {'title': '天天生鲜-用户中心', 'page': 1, 'userinfo': 0, 'userName': userName,'his_list':his_list}

    else:
        context = {'title': '天天生鲜-用户中心', 'page': 1, 'userinfo': 0}

    return render(request, 'df_user/user_center_info.html', context)


@login_required
def user_center_order(request):

    user=request.user

    orderInfos=OrderInfo.objects.filter(user_id=user.id).order_by('-create_time')


    for i in orderInfos:

        goodsInfos=OrderGoods.objects.filter(order_id=i.order_id)

        i.goods=goodsInfos





    return render(request, 'df_user/user_center_order.html', {'title': '天天生鲜-用户中心_订单', 'page': 2,'orderInfos':orderInfos})


@login_required
def user_center_site(request):
    if request.GET.get('action') == 'edit':
        uid=request.GET.get('uid')
        user_infos = UserInfo.objects.get(id=uid)

        dizhi=user_infos.userAddr

        print(dizhi)

        a=dizhi.split('-')

        sheng_id=AreaInfo.objects.get(title=a[0]).id
        shi_id=AreaInfo.objects.get(title=a[1]).id
        xian_id=AreaInfo.objects.get(title=a[2]).id
        detial=a[3]


        context = {'userinfo': user_infos, 'sheng_id':sheng_id,'shi_id':shi_id,'xian_id':xian_id,'detial':detial, 'title': '天天生鲜-用户中心_收货地址', 'page': 3}
        return render(request, 'df_user/user_center_site_change.html', context)


    elif request.GET.get('action') == 'delate':
        uid=request.GET.get('uid')
        user_infos = UserInfo.objects.get(id=uid)
        user_infos.is_delate=True
        user_infos.save()
        user_center_site_url = reverse('user:user_center_site')
        return redirect(user_center_site_url)


    elif request.GET.get('action') == 'add':
        user_id = request.session.get('_auth_user_id')
        return render(request,'df_user/user_center_site_add.html',{'user_id':user_id})


    elif request.GET.get('action') == 'set_default':
        user_id = request.session.get('_auth_user_id')

        aid=request.GET.get('uid')
        addr=UserInfo.objects.get(id=aid)
        user=UserInfo.objects.filter(user_id=user_id,isShow=True)

        for i in range(0,len(user)):

            user[i].isShow=False
            user[i].save()

        addr.isShow = True
        addr.save()
        user_center_site_url = reverse('user:user_center_site')
        return redirect(user_center_site_url)
    else:
        user_id = request.session.get('_auth_user_id')
        # user = User.objects.get(id=user_id)
        user_info_obj = UserInfo.objects.filter(user_id=user_id,is_delate=0)
        # print(user_info_obj)
        infos=[]
        if len(user_info_obj) > 0:
            for i in user_info_obj:
                # user_info = UserInfo.objects.filter(user_id=user_id)
                infos.append(i)
            context = {'title': '天天生鲜-用户中心_收货地址', 'infos':infos,'page': 3}
        else:
            context = {'userinfo': 0, 'title': '天天生鲜-用户中心_收货地址', 'page': 3}

        return render(request, 'df_user/user_center_site.html', context)


def User_revamp(request):
    user_id = request.session.get('_auth_user_id')
    uid = request.POST.get('uid')
    # user_id = request.session.get('_auth_user_id')
    shoujianren = request.POST.get('shoujianren')
    youbian = request.POST.get('youbian')
    shouji = request.POST.get('shouji')
    dizhi = request.POST.get('dizhi')
    is_default=request.POST.get('is_default')

    print('dizhi',dizhi)

    sheng_id=request.POST.get('sheng')
    shi_id=request.POST.get('shi')
    xian_id=request.POST.get('xian')

    sheng = AreaInfo.objects.get(id=sheng_id).title
    shi = AreaInfo.objects.get(id=shi_id).title
    xian = AreaInfo.objects.get(id=xian_id).title

    dd = sheng + '-' + shi + '-' + xian + '-'


    if request.GET.get('action') == 'add':

        # sheng=AreaInfo.objects.get(id=sheng_id).title
        # shi=AreaInfo.objects.get(id=shi_id).title
        # xian=AreaInfo.objects.get(id=xian_id).title
        #
        # dd=sheng+'-'+shi+'-'+xian+'-'
        # print(dd)

        if is_default=='1':
            user = UserInfo.objects.filter(user_id=user_id, isShow=True)
            for i in range(0, len(user)):
                user[i].isShow = False
                user[i].save()
            UserInfo.objects.create(userAddr=dd+dizhi,userPhone=shouji,userShou=shoujianren,userYoubian=youbian,user_id=uid,isShow=True)
        else:
            UserInfo.objects.create(userAddr=dd+dizhi,userPhone=shouji,userShou=shoujianren,userYoubian=youbian,user_id=uid)


        user_center_site_url = reverse('user:user_center_site')
        return redirect(user_center_site_url)


    else:
        user1 = UserInfo.objects.get(id=uid)

        user1.userShou = shoujianren
        user1.userPhone = shouji
        user1.userAddr = dd+dizhi
        user1.userYoubian = youbian
        if is_default=='1':
            user1.isShow=True
        else:
            user1.isShow = False
        user1.save()
        # context={'title':'天天生鲜-用户中心_收货地址','url':request.path,'shoujianren':shoujianren,'shouji':shouji,'dizhi':dizhi,'youbian':youbian}
        user_center_site_url = reverse('user:user_center_site')

        # return render(request,'df_user/user_center_site.html',context)
        return redirect(user_center_site_url)


def yanzhengma(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 120
    height = 38
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0qwertyuiopasdfghjklmnbvcxz'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    request.session['yanzhengma'] = rand_str.lower()
    # 构造字体对象
    font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf', 30)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((12, 1), rand_str[0], font=font, fill=fontcolor)
    draw.text((37, 1), rand_str[1], font=font, fill=fontcolor)
    draw.text((62, 1), rand_str[2], font=font, fill=fontcolor)
    draw.text((90, 1), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    # request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def active(request):
    try:
        login_url = reverse('user:login')
        info = tms(settings.SECRET_KEY, 3600)

        get_url = request.GET.get('url')
        get_info = info.loads(get_url)
        user = User.objects.get(id=get_info['id'])

        user.is_active = 1
        user.save()

        return redirect(login_url)
    except SignatureExpired as e:
        return HttpResponse('链接已过期')
    except BadSignature as e:
        return HttpResponse('无效的链接')


def pwd_forget(request):
    return render(request, 'df_user/pwd_forget.html')


def info_yz(request):
    get_username = request.GET.get('uname')
    uname_check = User.objects.filter(username=get_username)
    if not uname_check.exists():
        return JsonResponse({'username': 1})
    else:
        return JsonResponse({'username': 0})


def info_yza(request):
    get_info = request.GET.get('info', '')
    if get_info != '':
        return render(request, 'df_user/yz_email.html', {'get_info': get_info})

        # return render(request,'df_user/yz_email.html')


def email_yz(request):
    get_info = request.GET.get('info', '')
    get_email = request.GET.get('email', '')
    uname_check = User.objects.get(username=get_info)
    email_check = uname_check.email
    if email_check == get_email:
        return JsonResponse({'email': 1})
    else:
        return JsonResponse({'email': 0})


def fsyzm(request):
    get_info = request.GET.get('info', '')
    get_email = request.GET.get('email', '')
    user = User.objects.get(username=get_info)

    info = tms(settings.SECRET_KEY, 3600)
    token = info.dumps({'id': user.id}).decode()
    active_url = 'http://192.168.12.181:8000/user/cpwd?url=' + token

    send_title = '天天生鲜-忘记密码'
    send_message = ''
    send_obj_list = [get_email]  # 收件人列表
    send_html_message = '<h1>用户：%s，点击链接完成操作</h1> <a href="%s">跳转</a>' % (get_info,active_url)

    celery_send_mail.delay(send_title, send_message, settings.EMAIL_FROM, send_obj_list, send_html_message)

    # send_statue = send_mail(send_title, send_message, settings.EMAIL_FROM, send_obj_list,
    #                         html_message=send_html_message)
    # # 发送状态,可用可不用
    # print(send_statue)

    return JsonResponse({'token': token})


def cpwd(request):
    if request.method == 'POST':
        try:
            get_info = request.POST.get('id')
            get_pwd = request.POST.get('pwd')

            info = tms(settings.SECRET_KEY, 3600)
            get_id = info.loads(get_info)

            user = User.objects.get(id=get_id['id'])
            user.set_password(get_pwd)
            user.save()

            return HttpResponse('ok')
        except SignatureExpired as e:
            return HttpResponse('链接已过期')
        except BadSignature as e:
            return HttpResponse('无效的链接')

    elif request.method == 'GET':
        get_url = request.GET.get('url')
        return render(request, 'df_user/cpwd.html', {'id': get_url})


def register_jump(request):
    return render(request, 'df_user/register_jump.html')




def area2(request, id):

    id1 = int(id)
    # print(id1)
    if id1 == 0:
        data = AreaInfo.objects.filter(parea__isnull=True)
    else:
        data = [{}]
    # print('data',data)
    list = []
    for area in data:
        list.append([area.id, area.title])
    # print('list',list)
    return JsonResponse({'data': list})


def city(request, id):
    # print(2222)
    id1 = int(id)
    data = AreaInfo.objects.filter(parea_id=id1)
    list = []
    for area in data:
        list.append({'id': area.id, 'title': area.title})

    content = {'data': list}
    # print(content)
    return JsonResponse({'data': list})


def dis(request, id):
    id1 = int(id)
    data = AreaInfo.objects.filter(parea_id=id1)
    list = []
    for area in data:
        list.append({'id': area.id, 'title': area.title})
    return JsonResponse({'data': list})