import pygame, sys, random

# ============================================================================= #

size = width, height = 288, 512
clock = pygame.time.Clock()
pipe_count = 0

# ============================================================================= #

# Creating pipes.
def create_pipes():
	pipe_y = random.choice(pipe_height)
	tope_pipe = pipe_surface.get_rect(midtop = (pipe_x, pipe_y))
	bottom_pipe = pipe_surface.get_rect(midbottom = (pipe_x, pipe_y - pipe_gap))
	global pipe_count 
	pipe_count += 1
	return tope_pipe, bottom_pipe

# Moving pipes.
def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= pipe_speed
	return pipes
	
# Drawing pipes.
def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom > 512:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)	

def is_collided(pipes):
	for pipe in pipes:
		if(pipe.colliderect(bird_rect)):
			return True

# ============================================================================= #

pygame.init()

# Game variables
gravity = 0.1
bird_movement = 0
jump = 5
score = 0
game_active = False

# Setting up game window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

# Setting up background image.
background_night = pygame.image.load("background-night.png")

# Setting up life of game
font = pygame.font.Font('freesansbold.ttf', 32)
gameover_screen = pygame.image.load("gameover.png")
startup_screen = pygame.image.load("message.png")

# Setting up base
base = pygame.image.load("base.png")
base_x = 0
base_y = 410

# Setting up bird
bird_mid = pygame.image.load("yellowbird-midflap.png")
bird_x = 50
bird_y = 205
bird_rect = bird_mid.get_rect(center = (bird_x, bird_y))

#Setting up pipes
pipe_surface = pygame.image.load("pipe-red.png")
pipe_x = 350
pipe_height = range(200, 320, 10)
pipe_speed = 1.5
pipe_gap = 150
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# ============================================================================= #

# Game loop
while True:
	
	#Checking for events 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				bird_movement = 0
				bird_movement -= jump
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				game_active = True
		if event.type == SPAWNPIPE and game_active:
			pipes.extend(create_pipes())
			score += 1

	if not game_active:

		# Updating Background.
		screen.blit(background_night, (0, 0))
		screen.blit(startup_screen, (50, 40))
		screen.blit(gameover_screen, (50, 320))
		screen.blit(base, (0, 410))

	if game_active:

		# Updating Background.
		screen.blit(background_night, (0, 0))

		# Updateing pipes.
		pipes = move_pipes(pipes)
		draw_pipes(pipes)
		if (pipe_count > 3):
			pipes.pop(0)
			pipes.pop(1)
			pipe_count = 3

		# Updating base
		screen.blit(base, (base_x, base_y))
		screen.blit(base, (base_x + 336, base_y))
		base_x = base_x - 0.5
		if (base_x <= -336):
			base_x = 0

		# Updating bird
		screen.blit(bird_mid, bird_rect)
		bird_movement += gravity
		bird_rect.centery += bird_movement

		# Updating score on screen
		text = font.render(str(score), True, (255, 255, 255))
		text_rect = text.get_rect()
		text_rect.center = (140, 55)
		screen.blit(text, text_rect)

		# Collision detection.
		if(is_collided(pipes) or bird_rect.bottom >= base_y):
			bird_rect = bird_mid.get_rect(center = (bird_x, bird_y))
			pipes = []
			pipe_count = 0
			print ("Your score is " + str(score))
			score = 0
			game_active = False


	# Updating game window.
	pygame.display.update()
	clock.tick(120)

# ============================================================================= #
