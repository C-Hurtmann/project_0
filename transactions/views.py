from django.shortcuts import render
from django_tables2 import RequestConfig

from .models import Transaction
from .tables import TransactionTable


def transaction_list(request):
    table = TransactionTable(Transaction.objects.all())
    RequestConfig(request).configure(table)
    base_dir = (
        'partials/' if request.headers.get('HX-Request') else 'transactions/'
    )
    return render(
        request, f'{base_dir}transaction_list.html', {'table': table}
    )
