import django_tables2 as tables

from .models import Transaction


class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {'class': 'table table-striped'}
