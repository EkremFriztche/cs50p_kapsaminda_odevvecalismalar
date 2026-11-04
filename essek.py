import turtle
klm=turtle.Turtle()
turtle.speed(0)
turtle.bgcolor("magenta")
side=2
for i in range(2000):
    side=side+7
    klm.pendown()
    klm.color("blue")
    klm.circle(side)
    klm.left(45)
    klm.penup()