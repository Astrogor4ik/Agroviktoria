# Generated by Django 4.0.5 on 2022-07-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0003_alter_product_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_2',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
