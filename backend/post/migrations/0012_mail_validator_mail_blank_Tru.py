# Generated by Django 3.1.4 on 2020-12-24 14:12

from django.db import migrations
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_email_lower_case_phone_validator_blank_True'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=post.models.LowercaseEmailField(blank=True, max_length=254, null=True, validators=[post.models.mail_validator]),
        ),
    ]
