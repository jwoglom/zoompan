from vispy import app
from vispy.scene import SceneCanvas
from vispy.scene.visuals import Polygon
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

vertices = []
polygons = []

with open("xy00009.txt") as f:
    # skip vertex count
    f.next()
    for l in f:
        vertices.append(tuple(float(i) for i in l.strip().split()[-2:]))

print(vertices)

with open("el00009.txt") as f:
    # skip polygon count
    f.next()
    for l in f:
        t = [int(i) for i in l.strip().split()]
        # ignore lines for now
        if not any(i < 0 for i in t):
            polygons.append(Polygon([vertices[i] for i in t], color=red,
                            border_color=white, parent=v.scene))

app.run()
