# Generated by Django 4.2.3 on 2023-09-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=0),
        ),
    ]
