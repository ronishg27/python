import pygame, sys, random
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# Ball animation and collision
def ball_animation():
	global ball_x_speed, ball_y_speed, player_score, opponent_score, score_time

	ball.x += ball_x_speed
	ball.y += ball_y_speed

	if ball.top <= 0 or ball.bottom >= 718:	
		ball_y_speed *= -1

	if ball.left <= 0:
		player_score += 1
		score_time = pygame.time.get_ticks()
		
	if ball.right >= 1376:
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	if ball.colliderect(player) or ball.colliderect(opponent):
		ball_x_speed *= -1

# Border fo player
def p_border():
	if player.y <= 0:
		player.y = 0
	if player.y >= 718 - 150:
		player.y = 718 - 150

# Opponent AI
def opponent_ai():
	if opponent.top <= ball.y:
		opponent.top += opponent_speed
	if opponent.bottom >= ball.y:
		opponent.bottom -= opponent_speed

# Restart game
def ball_restart():
	global ball_x_speed, ball_y_speed, score_time

	current_time = pygame.time.get_ticks()
	ball.center = (width/2, height/2)

	if current_time - score_time < 700:
		number_three = time_font.render('3', False, light_grey)
		screen.blit(number_three, (width/2 - 17, height/2 - 80))

	if 700 < current_time - score_time < 1400:
		number_two = time_font.render('2', False, light_grey)
		screen.blit(number_two, (width/2 - 17, height/2 - 80))

	if 1400 < current_time - score_time < 2100:
		number_one = time_font.render('1', False, light_grey)
		screen.blit(number_one, (width/2 - 17, height/2 - 80))	

	if current_time - score_time < 2100:
		ball_x_speed, ball_y_speed = 0, 0

	else:
		ball_x_speed = 7 * random.choice((1, -1))
		ball_y_speed = 7 * random.choice((1, -1))
		score_time = None
	
	ball_x_speed *= random.choice((1, -1))
	ball_y_speed *= random.choice((1, -1))
	 

# Display
width = 1376
height = 718
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

# Rectangles
ball = pygame.Rect(width/2 - 50, height/2 , 40, 40)
player = pygame.Rect(width - 20,height/2 - 40, 15, 150)
opponent = pygame.Rect(5,height/2 - 40, 15, 150)

# Colors
bg_color = pygame.Color('darkslategray')
light_grey = (200, 200, 200)

# Game variables
ball_x_speed = 9 * random.choice((-1, 1))
ball_y_speed = 9 * random.choice((-1, 1))
player_speed = 0
opponent_speed = 13

# Sound
mixer.music.load('assets/251461__joshuaempyre__arcade-music-loop.wav')
mixer.music.play(-1)

# Text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 32)
time_font = pygame.font.Font('freesansbold.ttf', 64)

# Score timer
score_time = True


# Main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				player_speed -= 9
			if event.key == pygame.K_s:
				player_speed += 9
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				player_speed += 9
			if event.key == pygame.K_s:
				player_speed -= 9
	player.y += player_speed

	ball_animation()
	p_border()
	opponent_ai()

	# Visuals
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, light_grey, opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (width/2, 0), (width/2, height))

	if score_time:
		ball_restart()

	player_text = game_font.render(f'{player_score}', False, light_grey)
	screen.blit(player_text, (width/2 + 10, height/2 + 30))

	opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
	screen.blit(opponent_text, (width/2 - 25, height/2 + 30))

	pygame.display.update()
	clock.tick(60)
