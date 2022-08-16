from contextlib import contextmanager
from typing import Iterator
from typing import List
from typing import Union

import inkex

Color = Union[inkex.Color, str, int, None]

class Debug:
    def __init__(self, svg: inkex.SvgDocumentElement):
        self.svg = svg

    def clear(self) -> None:
        for rect in self.svg.xpath("/svg:svg/svg:rect"):
            rect.getparent().remove(rect)
        
    def draw_bbox(self, bbox: inkex.BoundingBox, color: Color = "red") -> None:
        rect = inkex.Rectangle.new(bbox.left, bbox.top, bbox.width, bbox.height)
        rect.style.update({
            "stroke": color,
            "stroke-width": "2",
            "fill": "none",
        })
        rect.set("sodipodi:insensitive", "true")
        self.svg.append(rect)


_debug: List[Debug] = []


@contextmanager
def debugger(svg: inkex.SvgDocumentElement) -> Iterator[None]:
    _debug.append(Debug(svg))
    try:
        yield
    finally:
        _debug.pop()


def draw_bbox(bbox: inkex.BoundingBox, color: Color = "red") -> None:
    if _debug:
        _debug[-1].draw_bbox(bbox, color=color)


def clear() -> None:
    if _debug:
        _debug[-1].clear()