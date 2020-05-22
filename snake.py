import pygame
import random
pygame.init()

size = width, height = 300, 300
win = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')

background_color = (63, 63, 68)
head_color = (255, 0, 0)
body_color = (247, 247, 247)
food_color = (204, 234, 187)

cell_size = 10
game_board = [[0 for _ in range(width//cell_size)] for _ in range(height//cell_size)]

font = pygame.font.Font('freesansbold.ttf', 12)

def set_food():
	global food
	a,b = random.randint(0,len(game_board[0])-1), random.randint(0,len(game_board)-1)
	while (b,a) in p.location:
		a,b = random.randint(0,len(game_board[0])-1), random.randint(0,len(game_board)-1)
	food = (b, a)

def move():
	keys = pygame.key.get_pressed()
	moved = False

	if keys[pygame.K_RIGHT] and p.direction != 1 and p.direction != 3:
		n = [(p.location[0][0], p.location[0][1]+1)]
		n.extend(p.location[0:-1])
		p.location = n
		p.direction = 1
		moved = True
	elif keys[pygame.K_DOWN] and p.direction != 2 and p.direction != 4:
		n = [(p.location[0][0]+1, p.location[0][1])]
		n.extend(p.location[0:-1])
		p.location = n
		p.direction = 2
		moved = True
	elif keys[pygame.K_LEFT] and p.direction != 3 and p.direction != 1:
		n = [(p.location[0][0], p.location[0][1]-1)]
		n.extend(p.location[0:-1])
		p.location = n
		p.direction = 3
		moved = True
	elif keys[pygame.K_UP] and p.direction != 4 and p.direction != 2:
		n = [(p.location[0][0]-1, p.location[0][1])]
		n.extend(p.location[0:-1])
		p.location = n
		p.direction = 4
		moved = True

	if not moved:
		if p.direction == 1:
			n = [(p.location[0][0], p.location[0][1]+1)]
			n.extend(p.location[0:-1])
			p.location = n
		elif p.direction == 2:
			n = [(p.location[0][0]+1, p.location[0][1])]
			n.extend(p.location[0:-1])
			p.location = n
		elif p.direction == 3:
			n = [(p.location[0][0], p.location[0][1]-1)]
			n.extend(p.location[0:-1])
			p.location = n
		elif p.direction == 4:
			n = [(p.location[0][0]-1, p.location[0][1])]
			n.extend(p.location[0:-1])
			p.location = n

def grow():
	l = p.location[-1]
	move()
	p.location.append(l)
	p.s += 1
	set_food()

def draw():
	win.fill(background_color)
	for r, c in p.location:
		pygame.draw.rect(win, body_color, (c*cell_size, r*cell_size, cell_size, cell_size))
	pygame.draw.rect(win, food_color, (food[0]*cell_size, food[1]*cell_size, cell_size, cell_size))
	text = font.render('Size: ' + str(p.s), True, food_color, background_color)
	win.blit(text, (width-50, 10))
	pygame.display.update()

class Player():
	def __init__(self, r, c, s):
		self.r = r
		self.c = c
		self.s = s
		self.location = [(r,c-i) for i in range(s)]
		self.direction = 1

p = Player(5, 5, 3)
set_food()

run = True
while run:
	pygame.time.delay(100)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	move()

	x, y = p.location[0]

	if (x,y) in p.location[1:] or (x < 0 or x >= len(game_board[0])) or (y < 0 or y >= len(game_board)):
		run = False
	if (x,y) == (food[1], food[0]):
		grow()

	draw()

pygame.quit()