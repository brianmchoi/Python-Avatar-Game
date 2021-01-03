# Make sure following libraries are installed
import pygame
from pygame import mixer
import random
import math
print("pygame imported\n")

# initialize pygame
pygame.init()

# create screen (height, width)
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("bg.png")

# music
mixer.music.load("main.wav")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Avatar Game")
icon = pygame.image.load("appa_icon_red.png")
pygame.display.set_icon(icon)

# CHANGE MANUAL

target_score = 10
num_lives = 3

# player

playerImg = pygame.image.load("aang_char_3_final.png")
playerX = 362
playerY = 500
playerX_change = 0
playerY_change = 0


# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load("zuko_char_1_final.png"))
  enemyX.append(random.randint(0,735))
  enemyY.append(random.randint(0, 50))
  enemyX_change.append(.5)
  enemyY_change.append(65)


# fireball

fireImg = []
fireX = []
fireY = []
fireX_change = []
fireY_change = []
num_of_fire = 10

for i in range(num_of_fire):
  fireImg.append(pygame.image.load("fireball.png"))
  fireX.append(random.randint(0,735))
  fireY.append(random.randint(0, 10))
  fireX_change.append(random.uniform(-0.25, 0.25))
  fireY_change.append(random.uniform(0.5, 1))


# air
# ready - can't see airball ; fire - airball is moving
airImg = pygame.image.load("airball.png")
airX = 0
airY = 500
airX_change = 0
airY_change = 1.5
air_state = "ready"


# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 24)

textX = 10
textY = 10

lives_value = num_lives


# game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
  over_text = over_font.render("DEFEAT", True, (255,255,255))
  screen.blit(over_text, (250,250))

def game_win_text():
  over_text = over_font.render("VICTORY", True, (255,255,255))
  screen.blit(over_text, (250,250))

def show_lives(x, y):
  lives = font.render("Lives: " + str(lives_value), True, (255,255,255))
  screen.blit(lives, (x,y))

def show_score(x, y):
  score = font.render("Score: " + str(score_value), True, (255,255,255))
  screen.blit(score, (x,y))

def player(x, y):
  screen.blit(playerImg, (x, y))

def enemy(x, y, i):
  screen.blit(enemyImg[i], (x, y))

def fire(x, y, i):
  screen.blit(fireImg[i], (x,y))

def attack(x, y):
  global air_state
  air_state = "fire"
  screen.blit(airImg, (x+16, y+10))

def isCollision(enemyX, enemyY, airX, airY):
  distance = math.sqrt(math.pow(enemyX-airX,2) + math.pow(enemyY-airY,2))
  if distance < 27:
    return True
  else:
    return False


def isHit(playerX, playerY, fireX, fireY):
  distance = math.sqrt(math.pow(playerX-fireX,2) + math.pow(playerY-fireY,2))
  if distance < 27:
    return True
  else:
    return False
  



running = True
# game loop
while running:

  # rgb - red, green, blue (0-255)
  screen.fill((50,0,0))
  screen.blit(background, (0,0))


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # player movement
    if event.type == pygame.KEYDOWN:
      #print("Keystroke pressed")

      if event.key == pygame.K_LEFT:
        #print("Left arrow")
        playerX_change = -1.5

      if event.key == pygame.K_RIGHT:
        #print("Right arrow")
        playerX_change = 1.5

      if event.key == pygame.K_UP:
        #print("Left arrow")
        playerY_change = -1.5

      if event.key == pygame.K_DOWN:
        #print("Right arrow")
        playerY_change = 1.5

      if event.key == pygame.K_SPACE:
        if air_state is "ready":
          attack_sound = mixer.Sound("air.flac")
          attack_sound.play()
          airX = playerX
          airY = playerY
          attack(airX, airY)


    # key raised
    if event.type == pygame.KEYUP:

      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #print("Keystroke released")
        playerX_change = 0

      if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #print("Keystroke released")
        playerY_change = 0

  playerX += playerX_change
  playerY += playerY_change

  # player boundary 
  if playerX <= 0:
    playerX = 0
  elif playerX >= 736:
    playerX = 736

  if playerY <= 440:
    playerY = 440
  elif playerY >= 536:
    playerY = 536




  # enemy boundary
  for i in range(num_of_enemies):

    # game over
    if enemyY[i] > 525 and score_value < target_score:
      
      enemyY[i] = 2000
      game_over_text()
      break


    enemyX[i] += enemyX_change[i]

    if enemyX[i] <= 0:
      enemyX_change[i] = .5
      enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
      enemyX_change[i] = -.5
      enemyY[i] += enemyY_change[i]

    # collision
    collision = isCollision(enemyX[i], enemyY[i], airX, airY)
    if collision and lives_value > 0: 
      oof_sound = mixer.Sound("oof.wav")
      oof_sound.play()
      airY = 500
      air_state = "ready"
      score_value += 1

      enemyX[i] = random.randint(0,735)
      enemyY[i] = random.randint(0, 50)
    
    enemy(enemyX[i], enemyY[i], i)


  # fire boundary
  for i in range(num_of_fire):

    #enemyX[i] += enemyX_change[i]
    fireY[i] += fireY_change[i]
    fireX[i] += fireX_change[i]

    if fireY[i] >= 600:
      fireY[i] = 0
      fireX[i] = random.randint(0, 735)

    # collision
    collision = isHit(playerX, playerY, fireX[i], fireY[i])
    if collision and score_value < target_score: 
      oof_sound = mixer.Sound("oof.wav")
      oof_sound.play()
      fireX[i] = random.randint(0,735)
      fireY[i] = random.randint(0, 50)
      #for j in range(num_of_fire):
        #fireY[j] = 2000
      if lives_value >= 1:
        lives_value -= 1
      else:
        lives_value == 0
      #break
    
    fire(fireX[i], fireY[i], i)


  # airball movement
  if airY <= 0:
    airY = 500
    air_state = "ready"
  if air_state is "fire":
    attack(airX, airY)
    airY -= airY_change

  if lives_value < 1 and score_value < target_score:
    game_over_text()

  if score_value >= target_score:
    game_win_text()

  player(playerX, playerY)

  show_score(textX, textY)
  show_lives(700, 10)

  pygame.display.update()
  