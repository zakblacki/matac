# Generated by Django 4.2.3 on 2023-07-29 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recui_image',
            field=models.ImageField(default='images/default.png', upload_to='orders_recu/'),
        ),
    ]
