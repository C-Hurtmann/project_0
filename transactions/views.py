from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .models import Transaction
from .tables import TransactionTable
from .filters import TransactionFilter


class TransactionListView(SingleTableMixin, FilterView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'transactions/transaction_list.html'
    filterset_class = TransactionFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['filter_applied'] = self.filterset.form.has_changed()
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['transactions/transaction_table_partial.html']
        return [self.template_name]
