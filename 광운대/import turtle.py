import turtle
from random import randint, choice

# 색상 리스트
green_shades = ['forest green', 'dark green', 'seagreen', 'lime green']
ornament_colors = ['red', 'blue', 'yellow', 'purple', 'orange']

# 원
def draw_circle(t, color, x, y, radius):
    t.penup()
    t.goto(x, y - radius)
    t.fillcolor(color)
    t.begin_fill()
    t.pendown()
    t.circle(radius)
    t.end_fill()

# 사각형
def draw_rectangle(t, color, x, y, width, height):
    t.penup()
    t.goto(x, y)
    t.fillcolor(color)
    t.begin_fill()
    t.pendown()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()

# 사다리꼴
def draw_trapezoid(t, color, x, y, top_width, height):
    bottom_width = top_width + 20
    t.penup()
    t.goto(x - top_width / 2, y + height)
    t.fillcolor(color)
    t.pencolor("red")
    t.begin_fill()
    t.pendown()
    t.goto(x + top_width / 2, y + height)
    t.goto(x + bottom_width / 2, y)
    t.goto(x - bottom_width / 2, y)
    t.goto(x - top_width / 2, y + height)
    t.end_fill()

# 별
def draw_star(t, color, x, y, size):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.color(color)
    t.begin_fill()
    t.pendown()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

# 전체 트리
def draw_christmas_tree():
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)

    # 트리 위치 설정
    start_y = 80
    last_y = 0

    # 🔁 줄기를 먼저 그려서 뒤로 보내기
    # 가지 높이 계산 먼저 해서 위치 예측
    total_levels = 7
    bottom_y = start_y - (total_levels - 1) * 25
    draw_rectangle(t, "saddlebrown", -15, bottom_y - 25, 30, 40)

    # 🎄 트리 가지 그리기
    for i in range(total_levels):
        top_width = 60 + i * 20
        y = start_y - i * 25
        draw_trapezoid(t, choice(green_shades), 0, y, top_width, 20)

    # 🎀 장식
    for _ in range(15):
        x = randint(-50, 50)
        y_random = randint(0, 100)
        draw_circle(t, choice(ornament_colors), x, y_random, 5)

    # ⭐ 별
    draw_star(t, "yellow", -10, 120, 30)

    # ✨ 작은 별 장식
    for _ in range(5):
        x = randint(-50, 50)
        y = randint(10, 120)
        draw_star(t, "gold", x, y, 10)

    # 📝 텍스트
    t.penup()
    t.goto(-85, 180)
    t.color("blue")
    t.write("Merry Christmas\nHappy New Year!", font=("Arial", 20, "italic"))

    # 🐢 좌우 거북이
    for pos in [-130, 110]:
        turtle_twin = turtle.Turtle()
        turtle_twin.shape("turtle")
        turtle_twin.color("green")
        turtle_twin.penup()
        turtle_twin.goto(pos, 180)

    t.hideturtle()
    screen.mainloop()

    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)

    # 텍스트
    t.penup()
    t.goto(-85, 180)
    t.color("blue")
    t.write("Merry Christmas\nHappy New Year!", font=("Arial", 20, "italic"))

    # 텍스트 양옆 거북이
    for pos in [-130, 110]:
        turtle_twin = turtle.Turtle()
        turtle_twin.shape("turtle")
        turtle_twin.color("green")
        turtle_twin.penup()
        turtle_twin.goto(pos, 180)

    # 트리 가지 (위에서 아래로 쌓기) + 마지막 y 좌표 기억
    start_y = 80
    last_y = 0  # 줄기 위치 계산용
    for i in range(7):
        top_width = 60 + i * 20
        y = start_y - i * 25
        draw_trapezoid(t, choice(green_shades), 0, y, top_width, 20)
        last_y = y  # 마지막 y 위치 저장

    # 트리 줄기 (가장 아래 가지보다 아래로)
    draw_rectangle(t, "saddlebrown", -15, last_y - 25, 30, 40)


    # 장식
    for _ in range(15):
        x = randint(-50, 50)
        y_random = randint(0, 100)
        draw_circle(t, choice(ornament_colors), x, y_random, 5)

    # 메인 별
    draw_star(t, "yellow", -10, 120, 30)

    # 장식용 작은 별
    for _ in range(5):
        x = randint(-50, 50)
        y = randint(10, 120)
        draw_star(t, "gold", x, y, 10)

    t.hideturtle()
    screen.mainloop()

# 실행
draw_christmas_tree()

