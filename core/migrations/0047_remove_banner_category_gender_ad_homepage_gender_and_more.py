# Generated by Django 5.0 on 2024-01-11 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_banner_category_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner_category',
            name='gender',
        ),
        migrations.AddField(
            model_name='ad_homepage',
            name='gender',
            field=models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE'), ('M-F', 'MALE-FEMALE'), ('E', 'ENFANTS')], default='F', max_length=3),
        ),
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 19, 0, 41, 182082)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 19, 0, 41, 160851)),
        ),
    ]
