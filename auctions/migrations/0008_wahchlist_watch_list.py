# Generated by Django 3.1.4 on 2020-12-19 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_wahchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wahchlist',
            name='watch_list',
            field=models.ManyToManyField(blank=True, related_name='watch_list', to='auctions.List'),
        ),
    ]
