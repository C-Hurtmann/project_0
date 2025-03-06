from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go

from collector.models import Transaction
from collector.utils import to_datetime


# Create your views here.
def home(request):
    transactions = Transaction.objects.all()

    x1 = [to_datetime(transaction.unix_time) for transaction in transactions]
    y1 = [(transaction.balance // 100) for transaction in transactions]
    
    trace = go.Scatter(
        x=x1,
        y=y1,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='rgba(78, 115, 223, 1)', width=2),
        marker=dict(size=6, color='rgba(78, 115, 223, 1)'),
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
            range=[min(x1), max(x1)],
            showgrid=True,
            gridcolor='rgba(234, 236, 244, 1)',
            zeroline=False
        ),
        yaxis=dict(
            title='Balance (UAH)',
            range=[min(y1) - 10, max(y1) + 10],
            showgrid=True,
            gridcolor='rgba(234, 236, 244, 1)',
            zeroline=False
        ),
        paper_bgcolor='rgba(255, 255, 255, 1)',
        plot_bgcolor='rgba(255, 255, 255, 1)',
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=40),
        # autosize=True
    )
    fig = go.Figure(data=[trace], layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    context = {'plot_div': plot_div}
    
    return render(request, 'dashboard/home.html', context)
