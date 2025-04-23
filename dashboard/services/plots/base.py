from abc import ABC
from dataclasses import dataclass
from typing import Any

from plotly import graph_objects as go
from plotly.offline import plot

from ..utils import Color


@dataclass
class Axis:
    title: str
    values: list[Any]
    color: str | None = None


class BasePlot(ABC):
    data: list
    layout: dict
    width: int = 800
    height: int = 400

    def __init__(self, title: str) -> None:
        self.title = title
        self.data = []
        self.layout = dict(
            title=dict(text=self.title, font=dict(size=18, color='#858796')),
            height=self.height,
            width=self.width,
            margin=dict(l=20, r=20, t=40, b=40),
            paper_bgcolor=str(Color.WHITE.value),
            plot_bgcolor=str(Color.WHITE.value),
        )

    @property
    def html(self) -> str:
        return plot(
            go.Figure(data=self.data, layout=self.layout), output_type='div'
        )
