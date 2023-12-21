# Generated by Django 4.2.3 on 2023-10-16 12:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_comments_and_ratings_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 12, 19, 4, 192592)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 12, 19, 4, 177983)),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderidpai',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
