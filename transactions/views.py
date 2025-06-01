from django.http import HttpResponse
from django.shortcuts import render
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .models import Transaction
from .tables import TransactionTable
from .filters import TransactionFilter
from .forms import TransferForm


class TransactionListView(SingleTableMixin, FilterView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'transactions/transaction_list.html'
    filterset_class = TransactionFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['transactions/transaction_list_partial.html']
        return [self.template_name]


def add_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)
    else:
        form = TransferForm()
    return render(
        request, 'transactions/transfer_form.html', {'form': form}
    )
