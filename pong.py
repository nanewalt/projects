import pygame
import math
import random
pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
font = pygame.font.Font('freesansbold.ttf', 24)

background_color = (63, 63, 68)
paddle_color = (247, 247, 247)
ball_color = (247, 247, 247)
inc = 25
ball_speed = 10
paddle_width = 10
maxAngle = 5 * math.pi / 12

class Paddle():
	def __init__(self, x, y, score=0):
		self.x = x
		self.y = y
		self.length = height // 4
		self.score = score


class Ball():
	def __init__(self, x, y, vel):
		self.x = x
		self.y = y
		self.vel = vel

def draw():
	screen.fill(background_color)
	s = 0
	m = width // 2
	while s < height:
		pygame.draw.line(screen, paddle_color, (m, s), (m, s+10), 3)
		s+= 15
	pygame.draw.rect(screen, paddle_color, (player.x, player.y, paddle_width, player.length))
	pygame.draw.rect(screen, paddle_color, (opponent.x, opponent.y, paddle_width, opponent.length))
	pygame.draw.rect(screen, ball_color, (ball.x, ball.y, paddle_width, paddle_width))
	player_score = font.render(str(player.score), True, paddle_color, background_color)
	opponent_score = font.render(str(opponent.score), True, paddle_color, background_color)
	screen.blit(player_score, (width // 2 - 40, 10))
	screen.blit(opponent_score, (width // 2 + 30, 10))
	pygame.display.update()

def init_vel():
	x_sin, y_sin = random.choice([-1, 1]), random.choice([-1, 1])
	x_nom, y_nom = x_sin * random.random(), y_sin * random.random()
	x_vel, y_vel = x_sin * ball_speed * math.cos(x_nom*maxAngle), y_sin * ball_speed * math.sin(y_nom*maxAngle)
	return (x_vel, y_vel)

def ball_collision():
	if ball.y < 0:
		ball.y -= 2 * ball.y
		ball.vel = (ball.vel[0], -1 * ball.vel[1])
	if ball.y + 10 > height:
		ball.y -= 2 * (ball.y + paddle_width - height)
		ball.vel = (ball.vel[0], -1 * ball.vel[1])
	if ball.x < 0:
		opponent.score += 1
		ball.x = width // 2
		ball.y = height // 2
		ball.vel = init_vel()
	if ball.x > width:
		player.score += 1
		ball.x = width // 2
		ball.y = height // 2
		ball.vel = init_vel()
	if ball.x <= player.x + paddle_width and ball.x >= player.x and ball.y >= player.y and ball.y <= player.y + player.length:
		bounceAngle = (((player.y + (player.length/2))- ball.y)/(player.length/2)) * maxAngle
		ball.vel = (ball_speed * math.cos(bounceAngle), ball_speed * math.sin(bounceAngle))
	if ball.x + paddle_width >= opponent.x and ball.x <= opponent.x + paddle_width and ball.y >= opponent.y and ball.y <= opponent.y + opponent.length:
		bounceAngle = (((opponent.y + (opponent.length/2))- ball.y)/(opponent.length/2)) * maxAngle
		ball.vel = (-ball_speed * math.cos(bounceAngle), ball_speed * math.sin(bounceAngle))

player = Paddle(20, height // 4)
opponent = Paddle(width - 30, height // 4)
ball = Ball(width // 2, height // 2, init_vel())

run = True
while run:
	pygame.time.delay(50)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_UP] and player.y - inc >= 0:
		player.y -= inc
	if keys[pygame.K_DOWN] and player.y + player.length + inc <= height:
		player.y += inc
	if opponent.y + (opponent.length // 2) < ball.y and opponent.y + opponent.length + inc <= height:
		opponent.y += inc
	if opponent.y + (opponent.length // 2) > ball.y and opponent.y - inc >= 0:
		opponent.y -= inc

	ball.x += ball.vel[0]
	ball.y += ball.vel[1]
	ball_collision()

	draw()

pygame.quit()