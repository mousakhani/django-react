import re
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.models import update_last_login
from django.core.validators import validate_email
from django.template.loader import get_template
import jwt
from hyperlink._url import NoneType
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api._serializer import UserSerializer, PostSerializer
from first import settings
from post.models import CustomUser, Post


class CreateUser(generics.CreateAPIView):
    '''
    '''
    # این دو کلاس به صورت پیش فرش در فایل settings.py تعریف شده است
    # authentication_classes = ()
    # permission_classes = ()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        # username validate
        if not data.get('username'):
            return Response(data={'username': 'نام کاربری الزامی است'}, status=status.HTTP_400_BAD_REQUEST)

        # phone validate
        phone = request.data.get('phone')
        if phone is not None and re.match('^09[0-9]{9}$', phone) is None:
            return Response(data={'phone': 'شماره تلفن صحیح نمی باشد'}, status=status.HTTP_400_BAD_REQUEST)

        # email validate
        email = request.data.get('email')
        if email.strip():
            try:
                user = CustomUser.objects.get(email=email)
                # اگر ایمیل ارسالی در حافظه باشد
                return Response(data={'email': 'این ایمیل ثبت شده است.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                # ایمیل نباشد یا بیش از یک بار تکرار شده باشد این بخش اجرا می شود
                # تکرار بیش از یک بار امکان ندارد مگر با دستکاری دستی دیتابیس
                pass
        else:
            # اگر ایمیل ارسال نشود
            return Response(data={'email': 'ایمیل الزامی است'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ایمیل بعد از تایید در دیتابیس ذخیره می شود
            user = CustomUser(
                username=data.get('username'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                adres=data.get('adres'),
                bio=data.get('bio'),
                avatar=data.get('avatar'),
                phone=data.get('phone'),
            )

            user.set_password(data.get('password'))
            user.save()

            Token.objects.create(user=user)
            # ایمیل آدرس فعلا ذخیره نمی شود
            # فقط برای ارسال ایمیل خط زیر نوشته شده است
            user.email = email
            # ارسال ایمیل برای تایید آدرس ایمیل
            #SendMail.send(user=user, mail_type='verify')
            # ایمیل نشان داده نشود. چون تصور می شود ثبت شده است
            user.email = ''
            data = self.get_serializer(user).data
            return Response({'user': data})

        except IntegrityError:
            # نام کاربری تکراری است
            return Response({'username': 'نام کاربری تکراری است'}, status=status.HTTP_400_BAD_REQUEST)

        except AttributeError:
            return Response({'email': 'ارسال ایمیل با مشکل مواجه شده است'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    '''
    نام کاربری و رمز عبور ارسال شده، توکن مربوطه دریافت می شود
    '''
    serializer_class = UserSerializer

    # لاگین شدن
    def post(self, request):
        '''
        ارسال نام کاربری و رمز عبور
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            update_last_login(None, user)
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'نام کاربری یا رمز عبور اشتباه می باشد'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileUser(APIView):
    '''
    استفاده و ویرایش پروفایل کاربر
    --------
    به لاگین نیاز دارد
    '''
    serializer_class = UserSerializer
    # دسترسی توسط توکن
    permission_classes = (IsAuthenticated,)

    # اپدیت پروفایل
    def put(self, request):
        # با استفاده از توکن ارسالی کاربر تشخیص داده شده است.
        # پس امکان ندارد کاربری وجود نداشته باشد
        try:
            user = CustomUser.objects.get(id=request.user.id)
            update = request.data.get('update').lower()
            if update == "data":
                return self.update_data(request, user)
            elif update == 'password':
                return self.update_password(request, user)
            else:
                return Response({'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        except:
            # خطای غیر قابل پیش بینی
            return Response(data={'update': 'please send update field'}, status=status.HTTP_400_BAD_REQUEST)

    def update_data(self, request, user):
        # update all data except the password
        # update all infoes
        data = request.data

        # تغییر نام کاربری
        # درخواست تغییر نام کاربری
        if data.get('username'):
            try:
                # اگر خط زیر دست اجرا شود، پس نمیتوان نام  کاربری درخواستی را به یوزر نسبت داد. چون همچین نامی وجود دارد
                CustomUser.objects.get(username=data.get('username'))
                return Response(data={'username': 'user name does exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                # اگر نام کاربری وارد نشود.
                # نام کاربری درصورتی که درخواست تغییر داده باشد، مهم است در غیر این صورت مهم نیست
                pass
                # اگر درخواست نام کاربری داده شود، و نام انتخابی در دیتابیس موجود نباشد، ادامه ی کد ها اجرا شود
            # درصورتی که درخواست تغییر نام کاربری داده شود، و نام انتخابی در دیتابیس موجود نباشد خط زیر اجرا خواهد شد
            user.username = data.get('username')

        # phone validate
        if data.get('phone'):
            if re.match('^09[0-9]{9}$', data.get('phone')) is None:
                return Response({'phone': 'شماره ی وارد شده صحیح نیست'}, status=status.HTTP_400_BAD_REQUEST)

        # email validate
        email = data.get('email')
        # درخواست تغییر ایمیل
        if email:
            # کاربر هنوز ایمیلش را تایید نکرده است
            if not user.email:
                return Response(data={'emial': 'ایمیل شما هنوز تایید نشده است'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            # ایمیل تکراری وارد نشود
            try:
                # ایمیل تکراری است
                # اگر ایمیل وارد شده مربوط به کاربر حاضر نباشد. نمی توان این ایمیل را به کاربر دیگر تخصیص داد پس
                email = email.strip()
                if CustomUser.objects.get(email=email).id != user.id:
                    return Response({'email': 'email does exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                # اگر ایمیل وارد شده در دیتابیس نباشد پس می توان ایمیل کاربر حاضر را به آن تغغیر داد
                pass
            try:
                validate_email(email)
            except Exception as err:
                # فرمت ایمیل درست نیست
                return Response({'email': err}, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     # فیلد ایمیل لازم است
            #     return Response({'email': 'Required'}, status=status.HTTP_411_LENGTH_REQUIRED)

        user.first_name = data.get('first_name') or user.first_name
        user.last_name = data.get('last_name') or user.last_name
        user.adres = data.get('adres') or user.adres
        user.bio = data.get('bio') or user.bio
        user.avatar = data.get('avatar') or user.avatar
        user.phone = data.get('phone') or user.phone
        # ایمیل تغییر یافته باید دوباره تایید شود
        if email and (user.email != email):
            # ایمیل مقداری پر و خالی می تواند داشته باشد
            user.email = email
            SendMail.send(user, mail_type='veify')
            user.email = ''
        user.save()
        return Response(data={'data': 'updated', "user": UserSerializer(user).data}, status=status.HTTP_200_OK)

    def update_password(self, request, user):
        try:
            password_validation.validate_password(request.data.get('password'))
        except Exception as err:
            return Response({'password': err}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'password': 'updated'}, status=status.HTTP_200_OK)


class AllPostList(generics.ListAPIView):
    '''
    لیست همه ی پست ها
    ---
    بدون نیاز به لاگین
    '''
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class Posts(APIView):
    '''
    کار با پستهای یوزر خاص
    '''
    permission_classes = (IsAuthenticated,)

    # درخواست لیست پست ها
    def get(self, request, post_pk=None):
        """
        get document of posts
        parameters
        -----
        request : str
                *request of client
        post_pk : int
                **post primary key
        return : 200
        """
        # زمانی که این متد فراخوانی شود یعنی توکن تایید شده است و
        # request.user
        # در دسترس قرار می گیرد.

        objs = Post.objects.filter(user_id=request.user.id)
        if post_pk:
            # اگر پست خاصی مد نظر باشد.
            objs = get_object_or_404(objs, pk=post_pk)
            # اگر پست خاص پیدا نشود.
        data = PostSerializer(objs, many=not post_pk).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        برای ذخیره کردن پست های کاربر خاصی از این متد استفاده می شود
        توجه شود که می توان درخواست های زیادی را پی در پی فرستاد که این موجب اخلال درکار وب سرویس خواهد کرد
        برای جلوگیری از این اتفاق باید یک timespan قرار داده شود.
        در production حتما این کار انجام شود.
        :param request:
        :return:
        """
        # اگر توکن صحیح نباشد، اصلا به این قسمت از کد نخواهیم رسید
        title = request.data.get('title')
        content = request.data.get('content')
        # فیلدهای title و content هم باید ارسال شوند و هم باید مقدار داشته باشند.
        if title is None or content is None or title.strip() == "" or content.strip() == "":
            return Response({'post': 'title or content is empty'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        title = request.data.get('title')
        content = request.data.get('content')
        try:
            post = Post(user=user, title=title, content=content)
            post.save()
        except:
            return Response({'post': 'post title is duplicated'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'id': post.pk, 'save': 'Ok'}, status=status.HTTP_201_CREATED)

    # update post
    def put(self, request, post_pk=None):
        # اگر توکن تایید نشود اصلا به این قسمت وارد نخواهد شد
        post = get_object_or_404(Post, pk=post_pk)
        post.title = request.data.get('title') or post.title
        post.content = request.data.get('content') or post.content
        post.save()
        data = PostSerializer(post).data
        return Response(data, status=status.HTTP_200_OK)

    # delete post
    def delete(self, request, post_pk=None):
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        return Response({'post': 'deleted'}, status=status.HTTP_200_OK)


class UserSearch(APIView):

    def get(self, request):
        data = request.data
        if data.get('search'):
            users = CustomUser.objects.filter(Q(username__contains=data.get('search')) |
                                              Q(first_name__contains=data.get('search')) |
                                              Q(last_name__contains=data.get('search'))).all()
            data_serialized = UserSerializer(users, many=True).data
            return Response(data_serialized, status=(status.HTTP_200_OK if users.count() > 0 else status.HTTP_404_NOT_FOUND))
        else:
            return Response({'search': 'Invalid value'}, status=status.HTTP_400_BAD_REQUEST)


class PostSearch(APIView):
    def get(self, request):
        data = request.data
        if data.get('search'):
            posts = Post.objects.filter(Q(title__contains=data.get('search')) | Q(content__contains=data.get('search')))
            data_serialized = PostSerializer(posts, many=True).data
            # اگر چیزی پیدا نشود، 404 ارسال می کند.
            return Response(data_serialized, status=(status.HTTP_200_OK if posts.count() > 0 else status.HTTP_404_NOT_FOUND))
        else:
            # اگر دیتا ارسال نشود 400 ارسال می کند.
            return Response({'search': 'Invalid value'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordRecovery(APIView):
    '''
    این بخش زمانی که کاربر لاگین نیست اجرا خواهد شد.
    '''

    def get(self, request):
        data = request.data
        try:
            # اگر ایمیل ثبت شده باشد
            email = data.get('email')
            user = CustomUser.objects.get(email=email)
            SendMail.send(user=user, mail_type='recovery')
        except:
            return Response({'email': 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'email': 'sent'}, status=status.HTTP_200_OK)


class SendMail:
    '''
    ارسال ایمیل برای تایید ایمیل و بازیابی رمز عبور
    '''

    @staticmethod
    def encoded_reset_token(data, mail_type='verify'):
        # فرصت برای تایید ایمیل هفت روز و برای بازیابی رمز عبور یک روز
        delta_seconds = settings.JWT_EXP_DELTA_SECONDS * (1 if mail_type == 'recovery' else 7)
        payload = {
            'user_id': data,
            'exp': datetime.utcnow() + timedelta(seconds=delta_seconds)
        }

        encoded_data = jwt.encode(
            payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        return encoded_data.decode('utf-8')

    @staticmethod
    def send(user, mail_type='verify'):
        # send email
        # مقادیر ارسالی مانند رمز عبور جدید و... را در قالب template قرار می دهد.
        # خط زیر برای تست فرانت اند کار قرار داده شده است
        if mail_type == 'recovery':
            base_url = 'http://localhost:8000/reset-password/'

            url = base_url + SendMail.encoded_reset_token(data=user.username, mail_type='recovery')

            rendered_message = get_template('verify_pass_or_recovery_mail.html').render({
                'url': url, 'username': user.username, 'mail_type': mail_type
            })
        else:
            # verify
            base_url = 'http://localhost:8000/mail-verify/'
            # ایدی و ایمیل برای تایید ایمیل لازم است. زمانی که کاربر لاگین نباشد و بخواهید ایمیلش را تایید کند، ایدی به کار می آید
            url = base_url + SendMail.encoded_reset_token(data={'username': user.username, 'email': user.email},
                                                          mail_type='verify')
            rendered_message = get_template('verify_pass_or_recovery_mail.html').render({
                'url': url, 'username': user.username, 'mail_type': mail_type
            })

        # fail_silently=True
        # پیش فرض False
        # اگر مقدار این False باشد، خطاهایی که هنگام ارسال ایمیل می تواند رخ دهد را نشان می دهد.
        # smtplib.SMTPException
        #
        # hmtl_message
        # اگر متن پیام از طریق این ارسال شود، به صورت یک سند html فرض شده، و تگهای html و کدهای css در ایمیل اجرا خواهند شد
        # اگر از طریق این ارسال نشود، تگها و کدها خود جزوی از متن پیام اسلی تلقی می شود.

        send_mail(subject='بازیابی رمز عبور' if mail_type == 'recovery' else 'تایید ایمیل', message='',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=(user.email,),
                  fail_silently=True,
                  html_message=rendered_message)


def decode_reset_token(reset_token):
    try:
        decoded_data = jwt.decode(reset_token, settings.JWT_SECRET,
                                  algorithms=[settings.JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None  # means expired token

    return decoded_data['user_id']


class ResetPassword(APIView):
    '''
    بازیابی رمز عبور
    '''

    def get(self, request, decoded_str):
        username = decode_reset_token(decoded_str)
        if id:

            # باید به یک صفحه ی پسورد جدید ریدایرکت شود
            return Response(
                {'username': username, 'token': Token.objects.get(user_id=CustomUser.objects.get(username=username).id).key},
                status=status.HTTP_200_OK)
        else:
            return Response({'token': 'لینک خراب می باشد'}, status=status.HTTP_400_BAD_REQUEST)



class VerifyMail(APIView):

    def get(self, request, decoded_str):
        '''
        زمانی که کاربر ایمیل دریافتی را کلیک می کند، در حالت پیش فرض دو مقدار ایدی و ایمیل از این کیلک دریافت می شود
        ایمیل در رکورد مربوط به ای دی ذخیره می شود
        در صورتی که دریافت نشود، یا لینک دستکاری شده، یا تاریخ انقضای لینک تمام شده است.
        '''
        data = decode_reset_token(decoded_str)
        if data:
            user_username = data['username']
            user_mail = data['email']
            user = CustomUser.objects.get(username=user_username)
            try:
                CustomUser.objects.get(email=user_mail)
                # اگر برای یک ایمیل دو کاربر درخواست کند و قبل از اینکه کاربر اول ایمیل را ثبت کند کاربر دوم درخواست دهد
                # به همریختگی ایجاد می شود
                # در اینحالت هر کاربری که ایمیل را زودتر ثبت کند، به نام آن است
                # اگر فقط یک بار ثبت شده باشد خطا را نشان بده
                return Response(data={'emial': 'این ایمیل ثبت شده است.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                # اگر ایمیل ارسال شده برای تایید ایمیل دوبار اجرا شود یا کس دیگری این ایمیل را ثبت کرده باشد
                # دیگر قابل اجرا نخواهد بود
                pass
            user.email = user_mail
            user.save()
            # باید به صفحه ی ایمیل تایید شد، ریدایرکت شود
            return Response({'email': 'ایمیل ثبت شد. باید به صفحه ی تایید ایمیل ریدایرکت کنم'}, status=status.HTTP_200_OK)
        # لینک دستکاری یا منقضی شده
        return Response({'email': 'لینک تایید ایمیل خراب می باشد'}, status=status.HTTP_404_NOT_FOUND)
