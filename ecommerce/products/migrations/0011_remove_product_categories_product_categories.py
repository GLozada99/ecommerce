# Generated by Django 4.0.6 on 2022-07-25 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_image_category_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='products.category'),
            preserve_default=False,
        ),
    ]