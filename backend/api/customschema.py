# # from drf_yasg import openapi
# from rest_framework import serializers
#
# from post.models import CustomUser
#
#

# class UserDrfSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password']
#
#
# profile_params = openapi.Parameter('update', openapi.IN_QUERY, description='توضیحات تست',
#                                    type=openapi.TYPE_BOOLEAN)
#
# auto_dict = {'operation_summary': 'پروفایل',
#              'operation_description': 'این یک توضیح برای این متد است',
#              'manual_parameters': [profile_params], 'responses': {404: 'Not Found'}}
#
# login_user_response = {200: openapi.Response('ایجاد شد', UserDrfSerializer)}
#
# create_user_params = openapi.Parameter('create', openapi.IN_QUERY, description='test create user', type=openapi.TYPE_STRING)
