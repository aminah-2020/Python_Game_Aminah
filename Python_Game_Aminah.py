import pgzrun
from random import *
#size of game window
WIDTH = 1000
HEIGHT = 600

#defining score and additional speed
score = 0
additional_speed = 0
level = 1

#defining image speeds
JUNK_SPEED = 5
SATELLITE_SPEED = 5
DEBRIS_SPEED = 5
LASER_SPEED = -7
#defining images
BACKGROUND_IMAGE = "python_game"

JUNK_IMG = "space_junk"

SATELLITE_IMG = 'my_junk_stuff'

DEBRIS_IMG = 'space_debris'

LASER_IMG = 'laser_red'

GAME_IMG = 'game_over'

LEVEL_IMG = 'level_up'

#background music
sounds.spacelife.play(-1)

# initialize junks
junks = [] # created a list to store our junks
score_board_height = 60
for i in range(5):  # make 5 junks
    junk = Actor(JUNK_IMG)
    x_pos = randint(-500, -50)
    y_pos = randint(score_board_height, HEIGHT - junk.height)
    junk.pos = (x_pos, y_pos)  # rect_position = (x, y)
    junks.append(junk)  # add each junk to our list

#initialize satellite sprite
satellite = Actor(SATELLITE_IMG)
x_sat = randint (-500, -50)
y_sat = randint ( score_board_height, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)

#initialize debris sprite
debris = Actor(DEBRIS_IMG)
x_deb = randint (-500, -50)
y_deb = randint ( score_board_height, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb)

#initialize lasers
lasers = [] #empty list


player = Actor('sprite_game')
player.midright = (WIDTH - 15, HEIGHT/2)

#updating junks, speed, collisions, and score.
def junk_update():
    global score
    global additional_speed
    global level
    score_board_height = 60
    for junk in junks:
        junk.x += JUNK_SPEED
        junk.x += additional_speed
        collision = player.colliderect(junk)
        if (junk.left > WIDTH or collision == 1):
            x_pos = randint(-150,-50)
            y_pos = randint(score_board_height, HEIGHT-junk.height)
            junk.topleft = (x_pos,y_pos)  
        if (collision==1):
            score+=1
            if (score >= 20 and score%20 == 0):
                level+=1
                additional_speed+=1
            sounds.collect_pep.play()
        
#updating satellite's motions, collisions, and points.
def satellite_update():
    global score
    global additional_speed
    global level
    satellite.x+= SATELLITE_SPEED
    satellite.x+= additional_speed

    collision = player.colliderect(satellite)
    if satellite.left > WIDTH or collision == 1:
        x_sat = randint (-500, -50)
        y_sat = randint (score_board_height, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score+= -10
        if (score >= 20 and score%20 == 0):
                level+=1
                additional_speed+=1
        sounds.explosion.play()

    

#updating debris' motions, collisions, and points.
def debris_update():
    global score
    global additional_speed
    global level
    debris.x+= DEBRIS_SPEED
    debris.x+= additional_speed
    collision = player.colliderect(debris)
    if debris.left > WIDTH or collision == 1:
        x_deb = randint (-500, -50)
        y_deb = randint (score_board_height, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score+= -5
        if (score >= 20 and score%20 == 0):
                level+=1
                additional_speed+=1
        sounds.explosion.play()

   
       
#updating player's motions   
def player_update():
    #keyboard input (up, down movement)
    if (keyboard.up == 1):
        player.y += (-5)
    elif (keyboard.down == 1):
        player.y += (5)
    #prevent player from moving through the top and bottom of screen
    if player.top < 60:
        player.top = 60
    
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    #spacebar = fire laser
    if keyboard.space == 1:
        laser = Actor (LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)


def laser_update():
    global score
    global level
    for laser in lasers:
        laser.x += LASER_SPEED
        #if laser goes off screen
        if laser.right < 0:
            lasers.remove(laser)
        #check for collisions
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = randint (-500, -50)
            y_sat = randint (score_board_height, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score+= -10
            if (score >=20 and score%20 ==0):
                level+=1
            sounds.explosion.play
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = randint (-500, -50)
            y_deb = randint (score_board_height, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score+=5
            if (score >=20 and score%20 ==0):
                level+=1
            sounds.explosion.play
        for junk in junks:
            if junk.colliderect(laser)== 1:
                lasers.remove(laser)
                x_pos = randint(-150,-50)
                y_pos = randint(score_board_height, HEIGHT-junk.height)
                junk.topleft = (x_pos,y_pos)
                score +=5
                if (score >=20 and score%20 ==0):
                level+=1
                sounds.explosion.play
        

def update():
    if score >=0:
        player_update()
        junk_update()
        satellite_update()
        debris_update ()
        laser_update()


Black = (0,0,0,)
def draw():
    screen.clear()
    #screen.fill(Red)
    screen.blit(BACKGROUND_IMAGE,(0,0))
    player.draw()
    debris.draw()
    satellite.draw()
    for junk in junks:
        junk.draw()
    for laser in lasers:
        laser.draw()
    if score < 0:
        game_over = "GAME OVER"
        screen.draw.text(game_over, center=(WIDTH/2, HEIGHT/2), fontsize=70, color="red", ocolor="white", owidth=0.5)
        sounds.spacelife.stop()
    
    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(700,15), fontsize = 35, color="black")
    show_level = "Level: " + str (level)
    screen.draw.text(show_level, topleft=(500,15), fontsize = 35, color="black")
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
    
pgzrun.go()
