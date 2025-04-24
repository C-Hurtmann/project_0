from plotly import graph_objects as go

from .base import BasePlot, Axis


class PiePlot(BasePlot):
    class_name: str = 'card-square'
    width: int = 375

    def __init__(self, title: str, categories: Axis, values: Axis) -> None:
        super().__init__(title)

        total = round(sum(values.values), 2)
        anotation_font_size = min(self.width, self.height) // 20

        self.data.append(
            go.Pie(
                labels=categories.values,
                values=values.values,
                hole=0.5,
                textinfo='none',
                marker=dict(
                    line=dict(
                        color='#FFFFFF', width=2  # White border around slices
                    )
                ),
                sort=True,
                direction='clockwise',
                showlegend=False
            )
        )
        self.layout.update(
            dict(
                annotations=[
                    dict(
                        text=f"Total<br>{total}",
                        font=dict(size=anotation_font_size, color='black'),
                        showarrow=False,
                        x=0.5,
                        y=0.5,
                        xref="paper",
                        yref="paper",
                        align="center"
                    )
                ],
            )
        )
