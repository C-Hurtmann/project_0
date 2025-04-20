import json
from datetime import date
from django.shortcuts import render
import pandas as pd

from transactions.models import Transaction
from .services.plots import ScatterPlot, PiePlot, Axis, BarPlot


# Create your views here.
def home(request):
    plot_divs = []
    # Data preparing for scatter
    transactions = pd.DataFrame(
        list(Transaction.objects.order_by('unix_time').values())
    )
    transactions['datetime'] = pd.to_datetime(
        transactions['unix_time'], unit='s'
    )
    transactions['date'] = transactions['datetime'].dt.date

    date_range = pd.date_range(
        transactions['date'].min(), date.today(), freq='D'
    ).date
    start_transaction = transactions[
        transactions['unix_time'] == transactions['unix_time'].min()
    ]
    start_balance = (
        start_transaction['balance'].iloc[0] -
        start_transaction['amount'].iloc[0]
    )

    result_by_date = pd.merge(
        pd.DataFrame({'date': date_range}),
        transactions.groupby('date')['amount'].sum().reset_index(),
        on='date',
        how='left'
    )
    result_by_date['amount'].fillna(0, inplace=True)
    result_by_date['balance'] = (
        result_by_date['amount'].cumsum() + start_balance
    )
    result_by_date['balance'] = (result_by_date['balance'] / 100).round(2)

    # Create scatter
    x = Axis(title='Date', values=result_by_date['date'].tolist())
    y = Axis(title='Balance (UAH)', values=result_by_date['balance'].tolist())

    scatter = ScatterPlot(title='Balance per day', x=x, y=y)
    plot_divs.append(scatter.html)

    # Data preparing for pie
    with open('resources/mcc.json') as f:
        mcc_description = json.load(f)

    expenses = transactions[transactions['amount'] < 0]
    expenses_by_mcc = expenses.groupby('mcc')['amount'].sum().reset_index()
    expenses_by_mcc['mcc_description'] = expenses_by_mcc['mcc'].apply(str).map(
        mcc_description
    ).fillna('Unknown')

    # Create pie
    categories = Axis(
        title='MCC', values=expenses_by_mcc['mcc_description'].tolist()
    )
    values = Axis(
        title='Expences',
        values=expenses_by_mcc['amount'].apply(abs).apply(
            lambda x: x / 100
        ).tolist()
    )
    pie = PiePlot(
        title='Expences distribution',
        categories=categories,
        values=values
    )

    plot_divs.append(pie.html)

    # create bar
    transactions['month'] = transactions['datetime'].dt.month
    transactions['year'] = transactions['datetime'].dt.year
    summary_by_month = transactions.groupby(['year', 'month'])['amount'].agg(
        income=lambda amount: amount[amount > 0].sum(),
        expences=lambda amount: amount[amount < 0].sum(),
    ).reset_index()

    x = Axis(title='Month', values=summary_by_month['month'].tolist())
    income = Axis(
        title='Income',
        values=(summary_by_month['income'] / 100).round(2).tolist(),
        color='#6AB187'
    )
    expences = Axis(
        title='Expences',
        values=(
            summary_by_month['expences'].apply(abs) / 100
        ).round(2).tolist(),
        color='#D32D41'
    )
    bar = BarPlot(f'Summary by Month {x.title}', x, income, expences)

    plot_divs.append(bar.html)

    context = {'plot_divs': plot_divs}
    return render(request, 'dashboard/home.html', context)
