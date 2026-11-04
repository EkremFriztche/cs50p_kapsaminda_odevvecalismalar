print("For the comparison of 'x' and 'y',")
while True:
    try:
        x = float(input("What's x? = " ))
        break
    except ValueError:
        print("Invalid input. Try again. ", end="")
while True:
    try:
        y = float(input("What's y? = "))
        break
    except ValueError:
        print("Invalid input. Try again. ", end="")
if x < y:
    print("x is less than y. ")
elif x > y:
    print("x is greater than y. ")
else:
    print("x is equal to y.")

#0.999999999999999999 = 1 (the count of 9s are 17 and above)

#This particular file of python is made by a beginner of coding, specifically a student that is new to python.
#As this is shown in my github profile, I don't seek any income and extra benefits from this project and it's continues.