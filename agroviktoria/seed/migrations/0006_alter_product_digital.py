# Generated by Django 4.0.5 on 2022-07-26 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0005_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=False, null=True, verbose_name='Послуга'),
        ),
    ]
