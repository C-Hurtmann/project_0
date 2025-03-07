from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

from collector.models import Transaction


# Create your views here.
def home(request):
    transactions = pd.DataFrame(list(Transaction.objects.order_by('unix_time').values()))
    transactions['date'] = pd.to_datetime(transactions['unix_time'], unit='s').dt.date

    date_range = pd.date_range(transactions['date'].min(), transactions['date'].max(), freq='D').date
    start_transaction = transactions[transactions['unix_time'] == transactions['unix_time'].min()]
    start_balance = start_transaction['balance'].iloc[0] - start_transaction['amount'].iloc[0]

    result_by_date = pd.merge(
        pd.DataFrame({'date': date_range}),
        transactions.groupby('date')['amount'].sum().reset_index(),
        on='date',
        how='left'
    )
    result_by_date['amount'].fillna(0, inplace=True)
    result_by_date['balance'] = result_by_date['amount'].cumsum() + start_balance
    result_by_date['balance'] = (result_by_date['balance'] / 100).round(2)


    x = result_by_date['date'].tolist()
    y = result_by_date['balance'].tolist()
    

    scatter = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(78, 115, 223, 0.3)',
        line=dict(
            color='rgba(78, 115, 223, 1)',
            width=3,
            shape='linear'
        ),
        hoverinfo='y',
        name='Balance'
    )
    layout = dict(
        title=dict(
            text='Balance per day',
            font=dict(size=18, color='#858796')
        ),
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='rgba(234, 236, 244, 1)',
            zeroline=False,
            rangeslider=dict(
                visible=True,
                thickness=0.05,
                bgcolor="lightgray",
                borderwidth=1,
                bordercolor="grey",
            )
        ),
        yaxis=dict(
            title='Balance (UAH)',
            showgrid=True,
            gridcolor='rgba(234, 236, 244, 1)',
            zeroline=False
        ),
        paper_bgcolor='rgba(255, 255, 255, 1)',
        plot_bgcolor='rgba(255, 255, 255, 1)',
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=40)
    )
    fig = go.Figure(data=[scatter], layout=layout)
    plot_div = plot(fig, output_type='div')
    context = {'plot_div': plot_div}
    
    return render(request, 'dashboard/home.html', context)
