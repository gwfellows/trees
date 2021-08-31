import turtle, tkinter

turtle.penup()
turtle.speed(0)
turtle.delay(0)


def draw(leaf_positions, branch_positions, sx=0, sy=300, r=2):
    for x, y in leaf_positions:
        #print(x, y)
        turtle.goto(x, y)
        turtle.pendown()
        turtle.circle(r)
        turtle.penup()
    for x1, y1, x2, y2 in branch_positions:
        #print(x1, y1, x2, y2)
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.goto(x2, y2)
        turtle.penup()
    turtle.goto(sx,sy)
    turtle.color("yellow")
    turtle.pendown()
    turtle.circle(3)
