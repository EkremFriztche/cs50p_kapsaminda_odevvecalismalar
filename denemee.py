import turtle as tosba
tosba.setup(640,640)
tosba.bgcolor("black")
ekran = tosba.Screen()
ekran.tracer(1, 0.9999999999999999)
zoom=590
G= 1.618
R= 1
tosba.speed(0)
tosba.up()
tosba.fd(230)
tosba.rt(90)
tosba.fd(120)
tosba.rt(90)
tosba.down()
for i in range(130000):
    zoom += R *G/3.2
    ekran.setworldcoordinates(-zoom, -zoom, zoom, zoom)
    tosba.pensize(1)
    tosba.color("gray")
    for j in range(4):
        tosba.fd(R)
        tosba.lt(90)
    tosba.pensize(2)
    tosba.color("yellow")    
    tosba.circle(R,90)
    R *=G
ekran.update()
tosba.done()