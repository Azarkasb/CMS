# Generated by Django 4.2.4 on 2023-08-16 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
        migrations.AddField(
            model_name='wallet',
            name='balance',
            field=models.BigIntegerField(default=0),
        ),
    ]
