# Generated by Django 5.1.5 on 2025-04-20 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatementFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('proccessed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'statement_files',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_id', models.CharField(max_length=255, unique=True)),
                ('unix_time', models.IntegerField()),
                ('mcc', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('operation_amount', models.IntegerField()),
                ('currency_code', models.IntegerField()),
                ('commission_rate', models.IntegerField()),
                ('balance', models.IntegerField()),
            ],
            options={
                'db_table': 'transactions',
                'ordering': ['id'],
            },
        ),
    ]
