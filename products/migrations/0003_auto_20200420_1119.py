# Generated by Django 3.0.2 on 2020-04-20 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200401_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='', max_length=50)),
                ('image', models.ImageField(default='', upload_to='media/')),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='URL',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('text', models.TextField(default='')),
                ('date', models.DateTimeField(auto_now=True)),
                ('like', models.CharField(blank=True, choices=[('like', 'like'), ('dislike', 'dislike')], max_length=150)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='products.Category'),
        ),
    ]
