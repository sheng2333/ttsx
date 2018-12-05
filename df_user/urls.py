"""Day URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views
urlpatterns = [


    url(r'^register/$', views.register,name='register'),
    url(r'^register_handle/$', views.register_handle,name='register_handle'),
    url(r'^login/$', views.user_login,name='login'),
    url(r'^loout/$', views.user_logout,name='user_logout'),
    # url(r'^login_handle/$', views.login_handle, name='login_handle'),
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^userName_exit/$', views.userName_exit, name='userName_exit'),
    url(r'^loginCheck/$', views.loginCheck, name='loginCheck'),
    url(r'^user_center_order/$', views.user_center_order, name='user_center_order'),
    url(r'^user_center_site$', views.user_center_site, name='user_center_site'),
    url(r'^userInfo_revamp/$', views.User_revamp, name='userInfo_revamp'),
    url(r'^email_exit/$', views.email_exit, name='email_exit'),
    url(r'^yanzhengma/$', views.yanzhengma, name='yanzhengma'),
    url(r'^check_yzm/$', views.check_yzm, name='check_yzm'),
    url(r'^active$', views.active, name='active'),
    url(r'^pwd_forget/', views.pwd_forget, name='pwd_forget'),
    url(r'^info_yz/', views.info_yz, name='info_yz'),
    url(r'^info_yza', views.info_yza, name='info_yza'),
    url(r'^email_yz', views.email_yz, name='email_yz'),
    url(r'^fsyzm', views.fsyzm, name='fsyzm'),
    url(r'^cpwd', views.cpwd, name='cpwd'),
    url(r'^register_jump', views.register_jump, name='register_jump'),


    url(r'^area/(\d+)', views.area2),
    url(r'^city=(\d+)', views.city),
    url(r'^dis=(\d+)', views.dis),
]
