# Generated by Django 4.0 on 2023-10-05 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_stock_loss_remove_stock_profit_user_loss_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_placed',
            name='order_date',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
    ]