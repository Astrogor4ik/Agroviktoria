# Generated by Django 4.0.5 on 2022-08-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0010_product_landing_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Призвіще'),
        ),
    ]
