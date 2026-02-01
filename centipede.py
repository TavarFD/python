import turtle
import math
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)  # Turn off automatic screen updates for smoother movement
screen.title("Skeletal Centipede")

# Create a custom C-shape for the segments
def create_c_shape(name, size):
    shape = ((0, 0), (size, 0), (size, size), (size * 0.8, size), (size * 0.8, size * 0.2), (0, size * 0.2))
    screen.register_shape(name, shape)

create_c_shape("c_shape", 40)  # Create a C-shape with a size of 20

# Mouse tracking
mouse_position = [0, 0]

# Function to track mouse movement continuously
def update_mouse_position(event):
    mouse_position[0] = event.x - screen.window_width() // 2
    mouse_position[1] = screen.window_height() // 2 - event.y

# Bind mouse movement to update mouse position
screen.getcanvas().bind('<Motion>', update_mouse_position)

# Create the centipede's skeletal body and legs
num_segments = 60  # Number of body segments
body = []
legs = []

# Create skeletal body segments
for i in range(num_segments):
    segment = turtle.Turtle()
    segment.shape("c_shape")  # Use the custom C-shape
    segment.color("white")  # White for the skeletal appearance
    segment.shapesize(0.5, 0.5)  # Thin and small body segments
    segment.penup()
    segment.speed(0)
    
    # Position the segments to create a spine
    segment.goto(i * 20 - (num_segments * 10), 0)
    body.append(segment)
    
    # Create legs for each segment
    leg_pair = []
    for j in range(2):  # Two legs per segment
        leg = turtle.Turtle()
        leg.shape("triangle")
        leg.color("gray")
        leg.shapesize(0.1, 1)  # Thin skeletal legs
        leg.penup()
        leg.speed(0)
        leg_pair.append(leg)
    legs.append(leg_pair)

# Tail for the last segment (smaller size)
tail = turtle.Turtle()
tail.shape("c_shape")  # Use the custom C-shape for the tail
tail.color("white")
tail.shapesize(0.3, 0.3)
tail.penup()
tail.speed(0)
tail.goto((num_segments - 1) * 20 - (num_segments * 10), 0)  # Position the tail
body.append(tail)

# Utility functions
def distance(point1, point2):
    """Calculate the distance between two points."""
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def move_centipede():
    # Move the head towards the mouse position gradually
    head = body[0]
    if distance([head.xcor(), head.ycor()], mouse_position) > 10:
        head_direction = head.towards(mouse_position[0], mouse_position[1])
        head.setheading(head_direction)
        head.forward(3)  # Control speed of movement

    # Move the rest of the body segments
    for i in range(1, len(body)):
        prev_segment = body[i - 1]
        cur_segment = body[i]
        if distance([cur_segment.xcor(), cur_segment.ycor()], [prev_segment.xcor(), prev_segment.ycor()]) > 10:
            cur_segment.setheading(cur_segment.towards(prev_segment))
            cur_segment.forward(3)

    # Animate the legs to crawl as the centipede moves
    for i, segment in enumerate(body[:-1]):
        leg_set = legs[i]
        # Left side leg
        leg_set[0].goto(segment.xcor() - 10, segment.ycor() - 6)
        leg_set[0].setheading(segment.heading() + 90)  # Make the legs perpendicular to the body
        # Right side leg
        leg_set[1].goto(segment.xcor() + 10, segment.ycor() - 6)
        leg_set[1].setheading(segment.heading() - 90)  # Make the legs perpendicular to the body
        # Leg motion (optional for animation)
        leg_set[0].forward(math.sin(time.time() * 10) * 2)  # Move legs in a crawling motion
        leg_set[1].forward(math.sin(time.time() * 10 + math.pi) * 2)

# Main loop for movement
while True:
    move_centipede()
    screen.update()
    time.sleep(0.02)  # Small delay for smoother movement

# Keep the window open
screen.mainloop()