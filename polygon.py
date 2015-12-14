# -*- coding: utf-8 -*-
# Copyright (c) 2015, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
Demonstration of PolygonVisual, EllipseVisual, RectangleVisual
and RegularPolygon
"""

from vispy import app
import sys
from vispy.scene import SceneCanvas
from vispy.scene.visuals import Polygon, Ellipse, Rectangle, RegularPolygon
from vispy.color import Color

white = Color("#ecf0f1")
gray = Color("#121212")
red = Color("#e74c3c")
blue = Color("#2980b9")
orange = Color("#e88834")

canvas = SceneCanvas(keys='interactive', title='Polygon Example',
                     show=True)
v = canvas.central_widget.add_view()
v.bgcolor = gray
v.camera = 'panzoom'

cx, cy = (0.2, 0.2)
halfx, halfy = (0.1, 0.1)

poly_coords = [(cx - halfx, cy - halfy),
               (cx + halfx + 0.5, cy - halfy),
               (cx + halfx, cy + halfy),
               (cx - halfx, cy + halfy)]
poly = Polygon(poly_coords, color=red, border_color=white,
               border_width=3,  parent=v.scene)

poly_coords2 = [(cx - halfx, cy - halfy),
               (cx + halfx + 0.5, cy - halfy),
               (cx + halfx, cy - 100),
               (cx - halfx, cy + halfy)]
poly2 = Polygon(poly_coords2, color=white, border_color=white,
               border_width=3,  parent=v.scene)

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()
