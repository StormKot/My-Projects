from turtle import *

screen = Screen()
screen.setup(800, 800)

pensize(8)

screen.onkey(lambda: forward(10), "Up")
screen.onkey(lambda: left(10), "Left")
screen.onkey(lambda: right(10), "Right")
screen.onkey(lambda: penup(), "u")
screen.onkey(lambda: pendown(), "d")
screen.onkey(lambda: clear(), "c")
screen.onkey(lambda: left(90), "9")

screen.listen()
done()
