# Generated by Django 5.1.4 on 2025-01-04 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
        migrations.AlterModelTable(
            name='transaction',
            table='transactions',
        ),
    ]
