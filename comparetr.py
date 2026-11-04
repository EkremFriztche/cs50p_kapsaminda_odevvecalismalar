print("'x' ve 'y' karşılaştırması için,")
while True:
    try:
        x = float(input("x nedir? = " ))
        break
    except ValueError:
        print("Yanlış girdi. Tekrar dene. ", end="")
while True:
    try:
        y = float(input("y nedir? = "))
        break
    except ValueError:
        print("Yanlış girdi. Tekrar dene. ", end="")
if x < y:
    print("x, y'den küçüktür. ")
elif x > y:
    print("x, y'den büyüktür. ")
else:
    print("x, y'ye eşittir/denktir. ")

#0.999999999999999999 = 1 (9 rakamının adedi 17 ve üstüdür)