# Generated by Django 3.0.14 on 2023-12-12 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клієнт', 'verbose_name_plural': 'Клієнти'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Замовлення', 'verbose_name_plural': 'Замовлення'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукти'},
        ),
        migrations.AlterModelOptions(
            name='reservation',
            options={'verbose_name': 'Бронювання', 'verbose_name_plural': 'Бронювання'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Відгук', 'verbose_name_plural': 'Відгуки'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'verbose_name': 'Місця', 'verbose_name_plural': 'Місця'},
        ),
    ]
