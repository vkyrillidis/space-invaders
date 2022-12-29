# Space Invaders
# python 2.7.12 on Mac
# Thanks to Christian Thompson
# Python Game Programming Tutorial: Space Invaders
# http://christianthompson.com/
import turtle
import math
import random
import winsound

# Set up the screen
win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.bgpic("space_invaders_background.gif")
win.tracer(0)

# Register the graphics for the game
turtle.register_shape("invader.gif")
turtle.register_shape("red_invader.gif")
turtle.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 100

# Score pen draws the score on stage
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)

# Middle of the screen message pen
middle_of_screen_pen = turtle.Turtle()
middle_of_screen_pen.speed(0)
middle_of_screen_pen.color("white")
middle_of_screen_pen.penup()
# Set position to middle of the screen
middle_of_screen_pen.setposition(0, 0)


def update_score():
    score_pen.clear()
    scorestring = f"Score: {score}"
    score_pen.write(scorestring, False, align="left", font=("Arial", 14, "bold"))
    score_pen.hideturtle()


def end_game_with_message(message):
    middle_of_screen_pen.clear()
    message = message.upper()
    middle_of_screen_pen.write(message, False, align="center", font=("Arial", 14, "bold"))
    middle_of_screen_pen.hideturtle()
    win.exitonclick()


# Draw the score initially
update_score()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.setposition(0, -250)
player.setheading(90)
player.speed = 15

# Choose number of enemies
number_of_enemies = 4

# Create an empty list of enemies
enemiesList = []


# Add enemies to the list
# We need to create more turtle objects
def create_new_enemy(color) -> turtle.Turtle():
    new_enemy = turtle.Turtle()
    new_enemy.shape("red_invader.gif" if color == "red" else "invader.gif")
    random_speed = max(random.randint(1, 3) * 0.1, 0.1)
    new_enemy.speed = random_speed
    new_enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    new_enemy.setposition(x, y)
    return new_enemy


for i in range(number_of_enemies):
    # Create the enemy
    enemiesList.append(create_new_enemy("green"))

# 1 means going to the right, -1 going to the left
direction = 1

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.speed(0)
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bullet.setposition(0, -400)

bulletspeed = 1

# Define bullet state
# we have 2 states:
# ready - ready to fire bullet
# fire - bullet is firing

bulletstate = "ready"


# Move the player left and right

def move_left():
    x = player.xcor()
    x = x - player.speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x = x + player.speed
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate and score as a global if it needs change
    global bulletstate, score
    if bulletstate == "ready":
        # os.system("afplay laser.wav&")
        # for linux use os.system("aplay laser.wav&")
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        bulletstate = "fire"
        # For each bullet fired, score -= 1
        score -= 1
        update_score()


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")


# Moves all enemies down 40 pixels
def move_enemies_down():
    for e in enemiesList:
        e.sety(e.ycor() - 40)


# Main game loop
while True:
    win.update()

    # Check if all enemies are destroyed
    if len(enemiesList) == 0:
        # Print game over
        end_game_with_message("You win!!!")

    # Check if enemies have reached the bottom of the screen
    for en in enemiesList:
        if en.ycor() < -250:
            print("GAME OVER")
            end_game_with_message("You lose!!!")

    for enemy in enemiesList:
        # This is a forever loop
        # Move the enemy
        enemy_speed = enemy.speed * direction
        x = enemy.xcor()
        x = x + enemy_speed
        enemy.setx(x)

        # Move all enemies back and down and change their direction
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            direction = direction * -1
            move_enemies_down()

        # Check for collision between bullet and enemy
        if isCollision(bullet, enemy):
            # os.system("afplay explosion.wav&")
            # for linux use os.system("aplay explosion.wav&")
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            if enemy.shape() == "invader.gif":
                # Green alien was hit, remove, create 2 red aliens and get 10 points
                enemiesList.remove(enemy)
                enemy.hideturtle()
                enemiesList.append(create_new_enemy("red"))
                enemiesList.append(create_new_enemy("red"))
                # Update the score
                score += 10
                update_score()
                continue
            else:
                # Red alien was hit, remove and get 20 points
                enemy.hideturtle()
                enemiesList.remove(enemy)
                score += 20
                update_score()

        # Check for collision between enemy and player
        if isCollision(player, enemy):
            # os.system("afplay explosion.wav&")
            # for linux use os.system("aplay explosion.wav&")
            winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
            player.hideturtle()
            enemy.hideturtle()
            print("GAME OVER")
            end_game_with_message("You lose!!!")
            break

    # Move the bullet only when bulletstate is "fire"
    if bulletstate == "fire":
        y = bullet.ycor()
        y = y + bulletspeed
        bullet.sety(y)

    # Check to see if bullet has reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

# delay = raw_input("Press enter to finish")
