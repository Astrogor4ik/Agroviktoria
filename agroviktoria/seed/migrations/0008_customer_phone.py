# Generated by Django 4.0.5 on 2022-07-31 14:08

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0007_product_top_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Номер телефону'),
        ),
    ]