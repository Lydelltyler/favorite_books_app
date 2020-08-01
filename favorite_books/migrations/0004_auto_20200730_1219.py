# Generated by Django 3.0.8 on 2020-07-30 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorite_books', '0003_auto_20200724_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favorites',
            field=models.ManyToManyField(related_name='fav_book', to='favorite_books.User'),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]