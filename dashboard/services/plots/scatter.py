from plotly import graph_objects as go

from .base import BasePlot, Axis
from ..utils import Color


class ScatterPlot(BasePlot):
    line_color: Color = Color.BLUE

    def __init__(self, title: str, x: Axis, y: Axis) -> None:
        super().__init__(title)
        self.data.append(
            go.Scatter(
                x=x.values,
                y=y.values,
                mode='lines',
                fill='tozeroy',
                fillcolor=str(self.line_color.value.shadow()),
                line=dict(
                    color=str(self.line_color.value), width=3, shape='linear'
                ),
                hoverinfo='skip',
                hovertemplate="%{y:.2f} UAH<br>Date : %{x}",
                name=self.title,
                showlegend=False
            )
        )
        self.layout.update(
            dict(
                xaxis=dict(
                    title=x.title,
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
                    title=y.title,
                    showgrid=True,
                    gridcolor='rgba(234, 236, 244, 1)',
                    zeroline=False
                ),
                hovermode='x unified',
            )
        )
