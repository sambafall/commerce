# Generated by Django 3.1.3 on 2021-01-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201231_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
