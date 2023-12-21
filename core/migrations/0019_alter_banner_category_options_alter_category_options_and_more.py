# Generated by Django 4.2.3 on 2023-10-16 08:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_matacor_info_contact_footer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner_category',
            options={'verbose_name': 'banner image pour un category ex(vettements, collection)', 'verbose_name_plural': 'banner image pour un category  ex(vettements, collection)'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categorie relie à des produit', 'verbose_name_plural': 'categories relie à des produit'},
        ),
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'coupon pour un produit', 'verbose_name_plural': 'coupon pour un produit'},
        ),
        migrations.AlterModelOptions(
            name='essential',
            options={'verbose_name': 'banner au centre de la page Home', 'verbose_name_plural': 'banners au centre de la page Home'},
        ),
        migrations.AlterModelOptions(
            name='excelfile',
            options={'verbose_name': "Produits à partir d'un fichier excel", 'verbose_name_plural': "Produits à partir d'un fichier excel"},
        ),
        migrations.AlterModelOptions(
            name='gendercategory',
            options={'verbose_name': 'Gender category ex(hommes,femmes..)', 'verbose_name_plural': 'Gender category ex(hommes,femmes..)'},
        ),
        migrations.AlterModelOptions(
            name='imageitem',
            options={'verbose_name': 'Image de Produit', 'verbose_name_plural': 'Images des Produits'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Produit', 'verbose_name_plural': 'Produits'},
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'verbose_name': 'Slide avec text et lien', 'verbose_name_plural': ' Slides avec texts et liens'},
        ),
        migrations.AlterModelOptions(
            name='topcategory',
            options={'verbose_name': 'category ex(Vettements,collections..)', 'verbose_name_plural': 'category ex(Vettements,collections..)'},
        ),
        migrations.AddField(
            model_name='order',
            name='orderidpai',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments_and_ratings',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 8, 32, 33, 500197)),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 8, 32, 33, 490246)),
        ),
    ]
