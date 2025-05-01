from django.db import models


# Create your models here.
class Transaction(models.Model):
    bank_id = models.CharField(max_length=255, unique=True)
    unix_time = models.IntegerField()
    mcc = models.IntegerField()
    amount = models.IntegerField()
    operation_amount = models.IntegerField()
    currency_code = models.IntegerField()
    commission_rate = models.IntegerField()
    balance = models.IntegerField()

    class Meta:
        db_table = 'transactions'
        ordering = ['-unix_time']


class StatementFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    proccessed = models.BooleanField(default=False)

    class Meta:
        db_table = 'statement_files'
