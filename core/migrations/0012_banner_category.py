# Generated by Django 4.2.3 on 2023-08-02 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_gendercategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.ImageField(upload_to='banner_imgs')),
                ('banner_link', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gendercategory')),
            ],
        ),
    ]
