import django_filters

from django.db.models import Q
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search')

    class Meta:
        model = Transaction
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return Transaction.objects.filter(Q(mcc=value) | Q(amount=value))
