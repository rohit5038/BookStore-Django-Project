# Generated by Django 5.0 on 2024-01-10 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0004_alter_book_bdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Action'), (2, 'Anime'), (3, 'Science-Fiction')], verbose_name='Category'),
        ),
    ]
