from plotly import graph_objects as go

from .base import BasePlot, Axis


class BarPlot(BasePlot):

    def __init__(self, title: str, x: Axis, *y: Axis) -> None:
        super().__init__(title)
        self.data.extend(
            [
                go.Bar(
                    x=x.values,
                    y=y_values.values,
                    name=y_values.title,
                    hovertemplate="%{y:.2f} UAH",
                    marker=dict(
                        color=y_values.color
                    ) if y_values.color else None
                ) for y_values in y
            ]
        )
        self.layout.update(
            dict(
                xaxis=dict(title=x.title),
                yaxis=dict(title='Summary'),
                barmode='group'
            )
        )
