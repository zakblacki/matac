# Generated by Django 5.0 on 2023-12-12 15:16

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_comments_and_ratings_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='formUrl',
            field=models.CharField(blank=True, default='', max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 12, 15, 16, 24, 614642)),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 12, 15, 16, 24, 596113)),
        ),
    ]
