import time
import math

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [["." for _ in range(width)] for _ in range(height)]
        
    def clear(self):
        self.pixels = [[" " for _ in range(self.width)] for _ in range(self.height)]
        
    def set_pixel(self, x, y, char):
        self.pixels[y][x] = char

    def draw_line(self, x1, y1, x2, y2, char="@"):
        dx = x2 - x1
        dy = y2 - y1
        
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            self.set_pixel(x1, y1, char)
            return
        
        for i in range(steps+1):
            t = i / steps
            
            x = round(x1 + dx * t)
            y = round(y1 + dy * t)
            
            self.set_pixel(x, y, char)
            
    def draw_triangle(self, p1, p2, p3, char="@"):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        
        min_x = max(0, min(x1, x2, x3))
        max_x = min(self.width - 1, max(x1, x2, x3))
        
        min_y = max(0, min(y1, y2, y3))
        max_y = min(self.height - 1, max(y1, y2, y3))
        
        def edge(a, b, p):
            return (p[0]- a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0]- a[0])
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                p = (x, y)
                
                w1 = edge(p2, p3, p)
                w2 = edge(p3, p1, p)
                w3 = edge(p1, p2, p)
                
                if(w1 >= 0 and w2 >= 0 and w3 >= 0) or (w1 <= 0 and w2 <= 0 and w3 <= 0):
                    self.set_pixel(x, y, char)

    def render(self):
        # print("\033[H\033[J", end="")
        
        for row in self.pixels:
            print("".join(row))
            
class Render3D:
    def __init__(self, screen):
        self.screen = screen
        self.scale = 20
        
    def project(self, point):
        x, y, z = point
   
        if z <= 0:
            return None
        
        x = x / z
        y = y / z
        
        screen_x = int(self.screen.width / 2 + x * self.scale)
        screen_y = int(self.screen.height / 2 + y * self.scale)
        
        return screen_x, screen_y
    
    def rotate_y(self, point, angle):
        x, y, z = point
        cos = math.cos(angle)
        sin = math.sin(angle)

        new_x = x * cos + z * sin
        new_y = y
        new_z = -x * sin + z * cos
        
        return new_x, new_y, new_z
    
    def draw_cube(self, center=(0, 0, 5), size=4, angle=0):
        cx, cy, cz = center
        h = size / 2

        vertices = [
            (-h, -h, -h),
            ( h, -h, -h),
            ( h,  h, -h),
            (-h,  h, -h),

            (-h, -h,  h),
            ( h, -h,  h),
            ( h,  h,  h),
            (-h,  h,  h)
        ]

        rotated_vertices = []

        for vertex in vertices:
            rotated = self.rotate_y(vertex, angle)

            x, y, z = rotated

            rotated_vertices.append(
                (x + cx, y + cy, z + cz)
            )

        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),

            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),

            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        ]

        projected = []

        for vertex in rotated_vertices:
            projected.append(self.project(vertex))

        for a, b in edges:
            p1 = projected[a]
            p2 = projected[b]

            if p1 is not None and p2 is not None:
                self.screen.draw_line(
                    p1[0],
                    p1[1],
                    p2[0],
                    p2[1],
                    "#"
                )
        
        
def run():
    WIDTH = 100
    HEIGHT = 40

    screen = Screen(WIDTH, HEIGHT)
    renderer = Render3D(screen)

    angle = 0

    while True:
        screen.clear()

        renderer.draw_cube(
            center=(0, 0, 5),
            size=4,
            angle=angle
        )

        screen.render()

        angle += 0.05

        time.sleep(0.03)


if __name__ == "__main__":
    run()