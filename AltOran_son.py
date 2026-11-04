import turtle as tosba
tosba.setup(550,550)
tosba.bgcolor("black")
ekran = tosba.Screen()
zoom=500
G= 1.618
R= 1
tosba.speed(0)
ekran.tracer(1, 0.99)
tosba.up()
tosba.fd(230)
tosba.rt(90)
tosba.fd(120)
tosba.rt(90)
tosba.down()
for i in range(1300000000):
    zoom += R *G/3.4
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

#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

#https://github.com/EkremFriztche