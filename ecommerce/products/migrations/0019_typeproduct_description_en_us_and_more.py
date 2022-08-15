# Generated by Django 4.0.6 on 2022-08-15 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_rename_description_product_general_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeproduct',
            name='description_en_us',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='typeproduct',
            name='description_es',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='typeproduct',
            name='name_en_us',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='typeproduct',
            name='name_es',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
