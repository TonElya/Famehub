# Generated by Django 2.1 on 2019-01-29 23:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190129_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 29, 23, 10, 8, 468172, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 29, 23, 10, 8, 516983, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='reset_token',
            field=models.CharField(default='pbkdf2:sha256:50000$UEzrIVam$da7d203d65ac9f4ebdbfa73c11850c4afba1bbd879f6f4e1a077b1edba9c6ad4', max_length=1000),
        ),
        migrations.AlterField(
            model_name='patron',
            name='email_token',
            field=models.CharField(default='pbkdf2:sha256:50000$IRNMFhsl$85b9428bf1a33ac08f1c131ad7e3571e83bbaed864247e478f0b86c7c2701758', max_length=1000),
        ),
    ]
