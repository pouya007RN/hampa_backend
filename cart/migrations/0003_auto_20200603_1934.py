# Generated by Django 3.0.5 on 2020-06-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]