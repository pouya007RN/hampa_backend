# Generated by Django 3.0.2 on 2020-04-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200420_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='URL',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='URL',
            field=models.TextField(default='', null=True),
        ),
    ]
