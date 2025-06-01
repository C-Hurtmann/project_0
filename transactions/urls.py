from django.urls import path
from .views import TransactionListView, add_transfer


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('/traansfers', add_transfer, name='add_transfer')
]
