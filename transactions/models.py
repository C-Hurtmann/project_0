from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


# Create your models here.
class StatementFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    proccessed = models.BooleanField(default=False)

    class Meta:
        db_table = 'statement_files'


class TransactionQuerySet(models.QuerySet):
    def visible(self):
        return self.exclude(
            Q(incoming_transfer__hidden=True) |
            Q(outcoming_transfer__hidden=True)
        )


class Transaction(models.Model):
    bank_id = models.CharField(max_length=255, unique=True)
    unix_time = models.IntegerField()
    mcc = models.IntegerField()
    amount = models.IntegerField()
    operation_amount = models.IntegerField()
    currency_code = models.IntegerField()
    commission_rate = models.IntegerField()
    balance = models.IntegerField()

    objects = models.Manager()
    visible = TransactionQuerySet().as_manager()

    class Meta:
        db_table = 'transactions'
        ordering = ['-unix_time']


class Transfer(models.Model):
    income = models.ForeignKey(
        Transaction,
        related_name='incoming_transfer',
        on_delete=models.CASCADE
    )
    outcome = models.ForeignKey(
        Transaction,
        related_name='outcoming_transfer',
        on_delete=models.CASCADE
    )
    difference_transaction = models.OneToOneField(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.income.amount <= 0:
            raise ValidationError({'income': 'Income must be > 0'})
        if self.outcome.amount >= 0:
            raise ValidationError({'outcome': 'Outcome must be < 0'})
        if self.income_id == self.outcome_id:
            raise ValidationError('Income and outcome must differ')
