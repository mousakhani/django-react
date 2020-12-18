from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class CustomUser(AbstractUser):
    class Meta:
        pass

    phone = models.CharField('شماره تلفن', max_length=11, null=True, blank=True)
    adres = models.TextField('آدرس', null=True, blank=True)
    desc = models.TextField('توضیحات', null=True, blank=True)
    avatar = models.ImageField('تصویر', upload_to='images', null=True, blank=True)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['password']

    def __str__(self):
        return f'{self.username}'

    #این متد برای نشان دادن عکس در پنل ادمین است.
    # برای کارکرد درست این متد، باید تغییراتی در فایل admin
    #داده شود
    #به فایل admin مراجعه شود
    def avatar_tag(self):
        #تابع format_html و mark_safe ورودی را به یک فایل html می چسبانند
        return format_html('<img src="%s" width="150px" height="150px" />' % (self.avatar.url))

    avatar_tag.short_description = 'تصویر'


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='deleted')
    title = models.CharField('عنوان', max_length=100,)
    content = models.TextField('محتوا')
    send_date = models.DateTimeField('تاریخ ارسال', auto_now_add=True)

    def __str__(self):
        return f'{self.title}-{self.user.username}'