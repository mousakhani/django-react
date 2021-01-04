from django.conf.urls import url
from django.urls import path, include, re_path, register_converter
from rest_framework import routers
from django.contrib.admin.templates import admin

from api.converters import EncodeTokenPathConverter
from api.views import (Posts, ListCreateUser, AllPostList, UserSearch,
                       PostSearch, PasswordRecovery, ResetPassword, VerifyMail, LoginUser, ProfileUser, UploadTest)

# router = routers.DefaultRouter()
# router.register('users', UserViewSets)

# خط زیر با استفاده از کلاسی که معرفی کردیم دیتای دریافتی از یو ار ال را چک می کند
register_converter(EncodeTokenPathConverter, 'token')

urlpatterns = [
    # path('user/list/', UserList.as_view(), name='user_list'),
    # path('user/<pk>/', user_detail, name='user_detail'),
    # path('', include(router.urls)),
    # -----------------------------------------------------------------------

    path('test/', UploadTest.as_view()),
    path('users/', ListCreateUser.as_view(), name='create_user'),
    # post لاگین کردن
    # put اپدیت کردن پروفایل
    path('users/login/', LoginUser.as_view(), name='user_login'),
    path('users/profile/', ProfileUser.as_view(), name='user_login'),

    # ([a-zA-z0-9-_.])+
    # جستوجو در نام کاربری، نام و نام خانوادگی
    # بدون نیاز به احراز هویت
    re_path(r'users/search/', UserSearch.as_view()),
    path('password-recovery/', PasswordRecovery.as_view()),
    # لینک ارسالی به کاربر برای ریست پسورد
    path('reset-password/<decoded_str>/', ResetPassword.as_view()),
    # لینک ارسالی به کاربر برای تایید ایمیل
    path('mail-verify/<decoded_str>/', VerifyMail.as_view()),
    # post لاگین کردن
    # put اپدیت کردن پروفایل
    path('users/login/', LoginUser.as_view(), name='user_login'),
    path('users/profile/', ProfileUser.as_view(), name='user_login'),

    # ------------------------------------------------------------------------

    path('posts/', AllPostList.as_view(), name='post_list'),
    re_path(r'posts/search/', PostSearch.as_view(), name='post_search'),

    # GETهمه ی پست های یک یوزر خاص را بر میگرداند
    # ایجاد پست جدید برای کاربر خاصPOST
    path('posts/user/', Posts.as_view(), name='post_detail'),

    # GETیک پست از یک یوزر خاص را بر می گرداند.
    # PUTویرایش یک پست از یک یوزر خاص
    # حذف یک پست از یک یوزر خاصِDELETE
    path('posts/user/<post_pk>/', Posts.as_view()),
    # جزئیات یک پست خاص
    # path('posts/detail/<pk>/', PostDetail.as_view(), name='post_detail')
]
