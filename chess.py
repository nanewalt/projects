import pygame
from itertools import cycle
import math
pygame.init()

cell_size = 64

size = width, height = cell_size*8, cell_size*8
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")

white_tile = (236, 210, 166)
black_tile = (166,118,81)
move_color = (6, 98, 59)
pieces = {
	1: pygame.transform.scale(pygame.image.load('assets/white_pawn.png'), (cell_size, cell_size)),
	2: pygame.transform.scale(pygame.image.load('assets/white_knight.png'), (cell_size, cell_size)),
	3: pygame.transform.scale(pygame.image.load('assets/white_bishop.png'), (cell_size, cell_size)),
	4: pygame.transform.scale(pygame.image.load('assets/white_rook.png'), (cell_size, cell_size)),
	5: pygame.transform.scale(pygame.image.load('assets/white_queen.png'), (cell_size, cell_size)),
	6: pygame.transform.scale(pygame.image.load('assets/white_king.png'), (cell_size, cell_size)),
	11: pygame.transform.scale(pygame.image.load('assets/black_pawn.png'), (cell_size, cell_size)),
	12: pygame.transform.scale(pygame.image.load('assets/black_knight.png'), (cell_size, cell_size)),
	13: pygame.transform.scale(pygame.image.load('assets/black_bishop.png'), (cell_size, cell_size)),
	14: pygame.transform.scale(pygame.image.load('assets/black_rook.png'), (cell_size, cell_size)),
	15: pygame.transform.scale(pygame.image.load('assets/black_queen.png'), (cell_size, cell_size)),
	16: pygame.transform.scale(pygame.image.load('assets/black_king.png'), (cell_size, cell_size))
	
}

def initialize():
	global game_board
	global white_turn
	global valid_positions
	global prev_moves
	global current_move
	white_turn = True
	game_board = [[0 for _ in range(8)] for _ in range(8)]
	game_board[0] = [14, 12, 13, 15, 16, 13, 12, 14]
	game_board[1] = [11, 11, 11, 11, 11, 11, 11, 11]
	game_board[6] = [1, 1, 1, 1, 1, 1, 1, 1]
	game_board[7] = [4, 2, 3, 5, 6, 3, 2, 4]
	valid_positions = set()
	prev_moves = []
	current_move = -1

def get_moves(r, c):
	pos = set()

	if white_turn:
		# WHITE PAWN
		if game_board[r][c] == 1:
			p1 = game_board[r-1][c]
			if r == 6:
				p2 = game_board[r-2][c]
			if c > 0:
				p3 = game_board[r-1][c-1]
			if c < 7:
				p4 = game_board[r-1][c+1]

			if p1 == 0:
				pos.add((r-1, c))
				if r == 6 and p2 == 0:
					pos.add((r-2, c))
			if c > 0 and p3 > 10:
				pos.add((r-1, c-1))
			if c < 7 and p4 > 10:
				pos.add((r-1, c+1))
		# WHITE KNIGHT
		elif game_board[r][c] == 2:
			possible = {(r-2, c-1),(r-1, c-2), (r-2, c+1), (r-1, c+2), (r+2, c-1), (r+1, c-2), (r+2, c+1), (r+1, c+2)}
			for x, y in possible:
				try:
					p = game_board[x][y]
					if p == 0 or p > 10:
						pos.add((x, y))
				except:
					pass
		# WHITE BISHOP
		elif game_board[r][c] == 3:
			for i in [-1, 1]:
				for j in [-1, 1]:
					p = [r, c]
					while True:
						p[0] += i
						p[1] += j
						try:
							if game_board[p[0]][p[1]] == 0:
								pos.add(tuple(p))
							else:
								if game_board[p[0]][p[1]] > 10:
									pos.add(tuple(p))
								break
						except:
							break
		# WHITE ROOK
		elif game_board[r][c] == 4:
			for i in [0, 1]:
				for j in [-1, 1]:
					p = [r, c]
					while True:
						p[i] += j
						try:
							if game_board[p[0]][p[1]] == 0:
								pos.add(tuple(p))
							else:
								if game_board[p[0]][p[1]] > 10:
									pos.add(tuple(p))
								break
						except:
							break
		# WHITE QUEEN
		elif game_board[r][c] == 5:
			game_board[r][c] = 3
			pos = pos.union((get_moves(r, c)))
			game_board[r][c] = 4
			pos = pos.union((get_moves(r, c)))
			game_board[r][c] = 5
		# WHITE KING
		elif game_board[r][c] == 6:
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					try:
						p = game_board[r+i][c+j]
						if p == 0 or p > 10:
							pos.add((r+i, c+j))
					except:
						pass

	else:
		# BLACK PAWN
		if game_board[r][c] == 11:
			p1 = game_board[r+1][c]
			if r == 1:
				p2 = game_board[r+2][c]
			if c > 0:
				p3 = game_board[r+1][c-1]
			if c < 7:
				p4 = game_board[r+1][c+1]

			if p1 == 0:
				pos.add((r+1, c))
				if r == 1 and p2 == 0:
					pos.add((r+2, c))
			if c > 0 and p3 > 0 and p3 < 7:
				pos.add((r+1, c-1))
			if c < 7 and p4 > 0 and p4 < 7:
				pos.add((r+1, c+1))
		# BLACK KNIGHT
		elif game_board[r][c] == 12:
			possible = {(r-2, c-1),(r-1, c-2), (r-2, c+1), (r-1, c+2), (r+2, c-1), (r+1, c-2), (r+2, c+1), (r+1, c+2)}
			for x, y in possible:
				try:
					p = game_board[x][y]
					if p == 0 or p < 7:
						pos.add((x, y))
				except:
					pass
		# BLACK BISHOP
		elif game_board[r][c] == 13:
			for i in [-1, 1]:
				for j in [-1, 1]:
					p = [r, c]
					while True:
						try:
							p[0] += i
							p[1] += j
							if game_board[p[0]][p[1]] == 0:
								pos.add(tuple(p))
							else:
								if game_board[p[0]][p[1]] < 7:
									pos.add(tuple(p))
								break
						except:
							break
		# BLACK ROOK
		elif game_board[r][c] == 14:
			for i in [0, 1]:
				for j in [-1, 1]:
					p = [r, c]
					while True:
						p[i] += j
						try:
							if game_board[p[0]][p[1]] == 0:
								pos.add(tuple(p))
							else:
								if game_board[p[0]][p[1]] < 7:
									pos.add(tuple(p))
								break
						except:
							break
		# BLACK QUEEN
		elif game_board[r][c] == 15:
			game_board[r][c] = 13
			pos = pos.union((get_moves(r, c)))
			game_board[r][c] = 14
			pos = pos.union((get_moves(r, c)))
			game_board[r][c] = 15
		# BLACK KING
		elif game_board[r][c] == 16:
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					try:
						p = game_board[r+i][c+j]
						if p == 0 or p < 7:
							pos.add((r+i, c+j))
					except:
						pass

	for a, b in pos.copy():
		if a < 0 or b < 0:
			pos.remove((a,b))
	return pos

def remove_invalid_moves(r, c, pos):
	global white_turn
	i = 0
	j = 16
	if white_turn:
		i = 10
		j = 6
	piece_pos = set()
	for y in range(8):
		for x in range(8):
			if game_board[y][x] > i and game_board[y][x] < i+7:
				piece_pos.add((y, x))
	v1 = game_board[r][c]
	game_board[r][c] = 0
	white_turn = not white_turn
	for p in pos.copy():
		end = False
		v2 = game_board[p[0]][p[1]]
		game_board[p[0]][p[1]] = v1
		for y, x in piece_pos:
			for m in get_moves(y, x):
				if game_board[m[0]][m[1]] == j:
					pos.remove(p)
					end = True
					break
			if end:
				break
		game_board[p[0]][p[1]] = v2
	game_board[r][c] = v1
	white_turn = not white_turn


def draw_moves(pos):
	for x, y in pos.copy():
		if game_board[x][y] == 6 or game_board[x][y] == 16:
			pos.remove((x, y))
		else:
			pygame.draw.circle(screen, move_color, (y*cell_size+cell_size//2, x*cell_size+cell_size//2), math.floor(math.sqrt(cell_size)))
	pygame.display.update()


def draw_board():
	screen.fill((0,0,0))
	tiles = cycle([white_tile, black_tile])
	for r in range(8):
		for c in range(8):
			pygame.draw.rect(screen, next(tiles), (c*cell_size, r*cell_size, cell_size, cell_size))
			if game_board[r][c] in pieces:
				screen.blit(pieces[game_board[r][c]], (c*cell_size, r*cell_size))
		next(tiles)
	pygame.display.update()

run = True
initialize()
draw_board()
while run:
	pygame.time.delay(50)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	select = pygame.mouse.get_pressed()

	if keys[pygame.K_LEFT] and current_move > -1:
		y, x, v1, r, c, v2 = prev_moves[current_move]
		game_board[y][x] = v1
		game_board[r][c] = v2
		white_turn = not white_turn
		current_move -= 1
		draw_board()
		pygame.time.delay(100)

	elif keys[pygame.K_RIGHT] and current_move < len(prev_moves) - 1:
		current_move += 1
		y, x, v1, r, c, v2 = prev_moves[current_move]
		game_board[y][x] = 0
		game_board[r][c] = v1
		white_turn = not white_turn
		draw_board()
		pygame.time.delay(100)

	elif select[0]:
		draw_board()
		mouse_position = pygame.mouse.get_pos()
		c = mouse_position[0] // cell_size
		r = mouse_position[1] // cell_size
		if (r, c) in valid_positions:
			y, x = selected_piece
			prev_moves = prev_moves[:current_move+1]
			prev_moves.append((y, x, game_board[y][x], r, c, game_board[r][c]))
			current_move += 1
			game_board[r][c] = game_board[y][x]
			game_board[y][x] = 0
			valid_positions.clear()
			white_turn = not white_turn
			draw_board()
		elif game_board[r][c]:
			selected_piece, valid_positions = (r, c), get_moves(r, c)
			remove_invalid_moves(r, c, valid_positions)
			draw_moves(valid_positions)
			
pygame.quit()


