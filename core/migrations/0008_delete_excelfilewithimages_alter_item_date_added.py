# Generated by Django 4.2.3 on 2023-08-06 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_excelfilewithimages_alter_item_date_added'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExcelFileWithImages',
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 22, 15, 29, 302520)),
        ),
    ]
