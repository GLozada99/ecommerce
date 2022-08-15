# Generated by Django 4.0.6 on 2022-08-15 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_long_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraDataProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('value', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_data', to='products.product')),
            ],
        ),
    ]