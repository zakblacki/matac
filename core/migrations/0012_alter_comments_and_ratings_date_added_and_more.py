# Generated by Django 4.2.3 on 2023-09-25 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_comments_and_ratings_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 25, 14, 44, 54, 676618)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 25, 14, 44, 54, 667234)),
        ),
    ]
