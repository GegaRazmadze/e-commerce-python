# Generated by Django 3.1.4 on 2020-12-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='category',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Books,Movies & Music', 'Books,Movies & Music'), ('Electronics', 'Electronics'), ('Collectibles & Art', 'Collectibles & Art'), ('Home & Garden', 'Home & Garden'), ('Sporting Goods', 'Sporting Goods'), ('Sporting Goods', 'Sporting Goods'), ('Businness & Industrials', 'Businness & Industrials'), ('Health & Beauty', 'Health & Beauty'), ('Others', 'Others')], max_length=255),
        ),
    ]
