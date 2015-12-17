import numpy as np

from vispy import app
from vispy import gloo

VS = """
attribute vec2 a_position;
attribute vec3 a_color;
varying vec3 v_color;
uniform mat3 u_view;

void main() {
    gl_Position = vec4((vec3(a_position, 1.)*u_view).xy, 0., 1.);
    v_color = a_color;
}
"""

FS = """
varying vec3 v_color;

void main() {
    gl_FragColor = vec4(v_color, 1.0);
}
"""

VSL = """
attribute vec2 a_position;
uniform mat3 u_view;

void main() {
    gl_Position = vec4((vec3(a_position, 1.)*u_view).xy, 0., 1.);
}
"""

FSL = """
void main() {
    gl_FragColor = vec4(1.0);
}
"""

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(600, 600), title='Zoom/Pan',
                            keys='interactive')

        self.x = 0
        self.y = 0
        self.scale = 1

        vertices = []
        self.polygons = []

        with open("xy00033.txt") as f:
            # skip vertex count
            f.next()
            for l in f:
                vertices.append(tuple(float(i) for i in l.strip().split()[-2:]))

        print(vertices)

        with open("el00033.txt") as f:
            # skip polygon count
            f.next()
            for l in f:
                t = [int(i) for i in l.strip().split()]
                # ignore lines for now
                if not any(i < 0 for i in t):
                    self.polygons.append([vertices[i] for i in t])

        print(self.polygons)

        positions = []
        for i in self.polygons:
            positions += [i[0],i[1],i[2],i[2],i[3],i[0]]

        positions_line = []
        for i in self.polygons:
            # lines will repeat, but it's a quick enough solution
            positions_line += [i[0],i[1],i[2],i[3],i[1],i[2],i[3],i[0]]

        self.blank = (0.1*np.ones((len(self.polygons),3))).astype(np.float32)
        self.colors = self.blank.copy()

        self.program = gloo.Program(VS, FS)
        self.program['a_position'] = positions
        self.program['a_color'] = np.repeat(self.colors, 6, axis=0)

        self.program_line = gloo.Program(VSL, FSL)
        self.program_line['a_position'] = positions_line

        self.activate_zoom()
        self.update_view()

        self.show()

    def on_draw(self, event):
        gloo.clear()
        self.program.draw(gloo.gl.GL_TRIANGLES)
        self.program_line.draw(gloo.gl.GL_LINES)

    def on_resize(self, event):
        self.activate_zoom()

    def activate_zoom(self):
        self.width, self.height = self.size
        gloo.set_viewport(0, 0, *self.physical_size)

    def update_view(self):
        self.program['u_view'] = [[self.scale,0,self.x*self.scale],
                                  [0,self.scale,self.y*self.scale],
                                  [0,0,1]]
        self.program_line['u_view'] = self.program['u_view']

    def on_mouse_move(self, event):
        if event.is_dragging and event.press_event.button == 1:
            delta = event.pos - event.last_event.pos
            self.x += 2*float(delta[0])/self.width/self.scale
            self.y += -2*float(delta[1])/self.height/self.scale
            self.update_view()
        mousex = (2*float(event.pos[0])/self.width-1)/self.scale-self.x
        mousey = -(2*float(event.pos[1])/self.height-1)/self.scale-self.y
        self.colors = self.blank.copy()
        for i in range(len(self.polygons)):
            if point_in_poly(mousex,mousey,self.polygons[i]):
                self.colors[i] = [1,1,1]
                for j in range(len(self.polygons)):
                    if len([k for k in self.polygons[j] if k in self.polygons[i]]) == 2:
                        self.colors[j] = [0.5,0.5,0.5]
                self.program['a_color'] = np.repeat(self.colors, 6, axis=0)
        self.update()

    def on_mouse_wheel(self, event):
        self.scale *= (1+0.05*event.delta[1])
        self.scale = max(0.0001,self.scale)
        self.on_mouse_move(event)
        self.update_view()
        self.update()

if __name__ == "__main__":
    c = Canvas()
    app.run()
