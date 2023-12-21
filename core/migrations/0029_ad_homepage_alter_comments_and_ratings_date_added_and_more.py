# Generated by Django 4.2.3 on 2023-10-29 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad_homePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AD_image', models.ImageField(upload_to='AD_imgs')),
                ('AD_link', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'AD home page',
                'verbose_name_plural': 'AD home page',
            },
        ),
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 14, 38, 1, 583137)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 14, 38, 1, 567979)),
        ),
    ]
