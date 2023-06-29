import turtle

def apply_rules(input_char):
    if input_char == 'F':
        return 'FF'
    elif input_char == 'X':
        return 'F+[[X]-X]-F[-FX]+X'
    else:
        return input_char

def process_string(old_str):
    new_str = ''
    for char in old_str:
        new_str = new_str + apply_rules(char)
    return new_str

def create_l_system(num_iters, axiom):
    start_string = axiom
    for i in range(num_iters):
        start_string = process_string(start_string)
    return start_string

def draw_l_system(turtle, instructions, angle, distance):
    stack = []
    for cmd in instructions:
        if cmd=='F':
            turtle.forward(distance)
        elif cmd=='B':
            turtle.backward(distance)
        elif cmd=='+':
            turtle.right(angle)
        elif cmd=='-':
            turtle.left(angle)
        elif cmd=='[':
            stack.append((turtle.position(), turtle.heading()))
        elif cmd==']':
            position, heading = stack.pop()
            turtle.penup()
            turtle.setposition(position)
            turtle.setheading(heading)
            turtle.pendown()

window = turtle.Screen()
leo = turtle.Turtle()
leo.speed(0)

l_system = create_l_system(5, "X")
draw_l_system(leo, l_system, 15, 2)

window.exitonclick()
