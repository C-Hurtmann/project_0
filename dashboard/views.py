from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go


# Create your views here.
def home(request):
    x1 = [1, 2, 3, 4, 5]
    y1 = [20, 35, 30, 20, 50]
    
    trace = go.Scatter(
        x=x1,
        y=y1,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='rgba(78, 115, 223, 1)', width=2),
        marker=dict(size=6, color='rgba(78, 115, 223, 1)'),
        hoverinfo='y',
        name='Earnings'
    )
    layout = dict(
        title=dict(
            text='Another Plot',
            font=dict(size=18, color='#858796')
        ),
        xaxis=dict(
            title='X-axis',
            range=[min(x1), max(x1)],
            showgrid=True,
            gridcolor='rgba(234, 236, 244, 1)',
            zeroline=False
        ),
        yaxis=dict(
            title='Y-axis',
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
