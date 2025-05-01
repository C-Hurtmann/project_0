import datetime
from decimal import Decimal, ROUND_HALF_UP

import django_tables2 as tables
from django.utils import timezone

from .models import Transaction
from .utils import mcc_to_category


class TransactionTable(tables.Table):
    id = tables.Column(accessor='bank_id', visible=False)
    date = tables.DateTimeColumn(accessor='unix_time', verbose_name='Date')
    category = tables.Column(accessor='mcc', verbose_name='Category')
    amount = tables.Column(verbose_name='Amount')

    class Meta:
        model = Transaction
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {'class': 'table table-striped'}
        fields = ('id', 'date', 'category', 'amount')

    def render_date(self, value):
        dt = datetime.datetime.fromtimestamp(
            value, tz=timezone.get_current_timezone()
        )
        return dt.strftime('%Y-%m-%d %H:%M')

    def render_category(self, value):
        return mcc_to_category(value)

    def render_amount(self, value):
        hryvnas = Decimal(value) / Decimal(100)
        return hryvnas.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
