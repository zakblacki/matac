# Generated by Django 5.0 on 2024-01-11 02:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_comments_and_ratings_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 3, 49, 37, 292795)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 3, 49, 37, 274971)),
        ),
        migrations.AlterField(
            model_name='item',
            name='id_item',
            field=models.IntegerField(default='0'),
        ),
    ]
