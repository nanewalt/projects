import pygame
import math
import random
pygame.init()

size = width, height = 920, 520
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
font = pygame.font.Font('freesansbold.ttf', 24)

background_color = (63, 63, 68)
paddle_color = (247, 247, 247)
ball_color = (247, 247, 247)
paddle_increment = 10
ball_speed = 15
paddle_width = 10
min_angle = 5 * math.pi / 180
max_angle = 60 * math.pi / 180

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
		self.prev = (width // 2, height // 2)

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
	y_sin = random.choice([-1, 1])
	x_vel = ball_speed * math.cos(random.random() * max_angle)
	y_vel = y_sin * math.sqrt(ball_speed**2 - x_vel**2)
	return (x_vel, y_vel)

def check_cross_width(A, B, C):
	return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def check_intersect(paddle):
	p1 = (ball.prev[0] + paddle_width // 2, ball.prev[1] + paddle_width // 2)
	p2 = (ball.x + paddle_width // 2, ball.y + paddle_width // 2)
	p3 = (paddle.x + paddle_width // 2, paddle.y)
	p4 = (paddle.x + paddle_width // 2, paddle.y + paddle.length)
	return check_cross_width(p1, p3, p4) != check_cross_width(p2, p3, p4) and check_cross_width(p1, p2, p3) != check_cross_width(p1, p2, p4)

def reflect(paddle):
	ball.x = paddle.x - 1
	x_sin = -1
	if paddle.x < width // 2:
		ball.x += paddle_width
		x_sin = 1
	ball.prev = (width//2, height//2)
	# ball.vel = (-ball.vel[0], ball.vel[1])
	if ball.vel[1] < 0: # UP
		intercept = paddle.y + paddle.length - (ball.y + paddle_width // 2)
		angle = min_angle + ((max_angle-min_angle) * (intercept / paddle.length))
		ball.vel = (x_sin * ball_speed * math.cos(angle), -ball_speed * math.sin(angle))
	else: 				# DOWN
		intercept = (ball.y + paddle_width // 2) - paddle.y
		angle = min_angle + ((max_angle-min_angle) * (intercept / paddle.length))
		ball.vel = (x_sin * ball_speed * math.cos(angle), ball_speed * math.sin(angle))
	
def ball_collision():
	if ball.y < 0:
		ball.y -= 2 * ball.y
		ball.vel = (ball.vel[0], -1 * ball.vel[1])
	elif ball.y + paddle_width > height:
		ball.y -= 2 * (ball.y + paddle_width - height)
		ball.vel = (ball.vel[0], -1 * ball.vel[1])
	elif ball.x < 0:
		opponent.score += 1
		ball.x = width // 2
		ball.y = height // 2
		ball.vel = init_vel()
	elif ball.x > width:
		player.score += 1
		ball.x = width // 2
		ball.y = height // 2
		ball.vel = init_vel()
	elif check_intersect(player):
		reflect(player)
	elif check_intersect(opponent):
		reflect(opponent)

player = Paddle(20, height // 4)
opponent = Paddle(width - 30, height // 4)
ball = Ball(width // 2, height // 2, init_vel())

run = True
while run:
	pygame.time.delay(10)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_UP] and player.y - paddle_increment >= 0:
		player.y -= paddle_increment
	if keys[pygame.K_DOWN] and player.y + player.length + paddle_increment <= height:
		player.y += paddle_increment
	if opponent.y + (opponent.length // 2) < ball.y and opponent.y + opponent.length + paddle_increment <= height:
		opponent.y += .9 * paddle_increment
	if opponent.y + (opponent.length // 2) > ball.y and opponent.y - paddle_increment >= 0:
		opponent.y -= .9 * paddle_increment

	ball.prev = (ball.x, ball.y)
	ball.x += ball.vel[0]
	ball.y += ball.vel[1]
	ball_collision()

	draw()

pygame.quit()