import turtle
import math
import time
import colorsys

# Cấu hình màn hình
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Trái tim hồng động")

# Tạo turtle
pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)
pen.hideturtle()

# Đổi màu theo thời gian
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Vẽ trái tim tại vị trí (x, y) với kích thước size và màu color
def draw_heart(x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for t in range(0, 360, 1):
        angle = math.radians(t)
        r = size * (1 - math.sin(angle))
        x_ = r * math.sin(angle)
        y_ = r * math.cos(angle)
        pen.goto(x + x_, y + y_)
    pen.end_fill()

# Hiệu ứng động trái tim
hue = 0
while True:
    pen.clear()
    for i in range(20):
        radius = 10 + i * 3
        rgb = hsv2rgb((hue + i * 0.05) % 1.0, 1.0, 1.0)
        hex_color = "#%02x%02x%02x" % rgb
        draw_heart(0, -radius, radius, hex_color)
    hue += 0.01
    time.sleep(0.05)
