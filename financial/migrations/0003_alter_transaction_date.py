# Generated by Django 4.2.4 on 2023-08-18 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0002_rename_transactions_transaction_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
