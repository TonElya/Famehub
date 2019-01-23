# Generated by Django 2.1 on 2019-01-23 13:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 13, 5, 15, 577188, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 13, 5, 15, 635793, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='reset_token',
            field=models.CharField(default='pbkdf2:sha256:50000$ChN8Ed2k$638360ef16026961544b567152b2b8d8d9d717adbd2d6fb1643e51e881f4342b', max_length=1000),
        ),
        migrations.AlterField(
            model_name='patron',
            name='email_token',
            field=models.CharField(default='pbkdf2:sha256:50000$kh9tddLQ$fa61b33095414412c80aa7d7980304f1a78f9316f0a5b71f961b122d189be455', max_length=1000),
        ),
    ]
