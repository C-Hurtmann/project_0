from django.db import models

# Create your models here.
class Transaction(models.Model):
    bank_id = models.CharField(max_length=255, unique=True)
    unix_time = models.IntegerField()
    mcc = models.IntegerField()
    original_mcc = models.IntegerField()
    amount = models.IntegerField()
    original_amount = models.IntegerField()
    currency_code = models.IntegerField()
    commission_rate = models.IntegerField()
    balance = models.IntegerField()
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
