# Generated by Django 4.0.5 on 2022-08-01 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0009_alter_product_content_alter_shippingaddress_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='landing_rate',
            field=models.IntegerField(null=True, verbose_name='Норма висадки(ручна)'),
        ),
    ]