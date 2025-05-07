from datetime import datetime

from django import forms
import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='unix_time',
        lookup_expr='gte',
        label='Start Date',
        method='filter_start_date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    end_date = django_filters.DateFilter(
        field_name='unix_time',
        lookup_expr='lt',
        label='End Date',
        method='filter_end_date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date']

    def filter_start_date(self, queryset, name, value):
        if value:
            start_datetime = datetime.combine(value, datetime.min.time())
            start_ts = int(start_datetime.timestamp())
            return queryset.filter(unix_time__gte=start_ts)
        return queryset

    def filter_end_date(self, queryset, name, value):
        if value:
            end_datetime = datetime.combine(value, datetime.max.time())
            end_ts = int(end_datetime.timestamp())
            return queryset.filter(unix_time__lt=end_ts)
        return queryset
