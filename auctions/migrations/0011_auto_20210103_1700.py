# Generated by Django 3.1.3 on 2021-01-03 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210103_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='Product_Name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_bids', to='auctions.auction'),
        ),
    ]
