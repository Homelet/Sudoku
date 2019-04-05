def calculate_region(x, y):
	if x <= 2:
		if y <= 2:
			return 0
		elif y <= 5:
			return 1
		else:
			return 2
	elif x <= 5:
		if y <= 2:
			return 3
		elif y <= 5:
			return 4
		else:
			return 5
	else:
		if y <= 2:
			return 6
		elif y <= 5:
			return 7
		else:
			return 8


class Node:
	def __init__(self, board, x, y, value=None):
		self._value = value
		self._board = board
		self._x = x
		self._y = y
		self._grid_number = calculate_region(x, y)
		if self._value is None:
			self._possible = [i for i in range(1, 10)]
		else:
			self._possible = []
	
	
	def reduce_possible(self, value):
		if value in self._possible:
			self._possible.remove(value)
	
	
	def stack_possible(self, value):
		if value in self._possible:
			self._possible.remove(value)
	
	
	def is_set(self):
		return self._value is not None
	
	
	def set_value(self, value):
		self._value = value
		self._board.refresh(self)
	
	
	def possible(self):
		return self._possible
	
	
	def possible_size(self):
		return self._possible.__len__()
	
	
	def value(self):
		return self._value
	
	
	def x(self):
		return self._x
	
	
	def y(self):
		return self._y
	
	
	def grid_number(self):
		return self._grid_number


class Board:
	def __init__(self, board):
		self._board = [[Node(self, x, y, value=board[x][y]) for x in range(9)] for y in range(9)]
		self._grids = [
			[node for line in self._board for node in line if node.grid_number() is 0],
			[node for line in self._board for node in line if node.grid_number() is 1],
			[node for line in self._board for node in line if node.grid_number() is 2],
			[node for line in self._board for node in line if node.grid_number() is 3],
			[node for line in self._board for node in line if node.grid_number() is 4],
			[node for line in self._board for node in line if node.grid_number() is 5],
			[node for line in self._board for node in line if node.grid_number() is 6],
			[node for line in self._board for node in line if node.grid_number() is 7],
			[node for line in self._board for node in line if node.grid_number() is 8],
		]
	
	
	def refresh(self, n):
		self.refresh_x(n.x(), n)
		self.refresh_y(n.y(), n)
		self.refresh_grid(n)
	
	
	def refresh_x(self, x, n):
		l_x = [line[x] for line in self._board]
		for c_node in l_x:
			if c_node.is_set():
				continue
			c_node.reduce_possible(n.value())
	
	
	def refresh_y(self, y, n):
		l_y = self._board[y]
		for c_node in l_y:
			if c_node.is_set():
				continue
			c_node.reduce_possible(n.value())
	
	
	def refresh_grid(self, n):
		l_grid = self._grids[n.grid_number()]
		for c_node in l_grid:
			if c_node.is_set():
				continue
			c_node.reduce_possible(n.value())
	
	
	def init_status(self):
		for line in self._board:
			for node in line:
				self.refresh(node)
	
	
	def debug(self):
		real_index = 0
		for x in range(13):
			for y in range(13):
				if x % 4 == 0:
					if y % 4 == 0:
						print("+", end="")
					else:
						print("---", end="")
				else:
					if y % 4 == 0:
						print("|", end="")
					else:
						value = self._board[real_index % 9][real_index // 9].value()
						if value is None:
							print("   ", end="")
						else:
							print(" " + str(value) + " ", end="")
						real_index += 1
			print("\n", end="")
	
	
	def find_next(self):
		next_node = None
		for line in self._board:
			for node in line:
				if node.is_set():
					continue
				if next_node is None or node.possible_size() < next_node.possible_size():
					next_node = node
		return next_node
	
	
	def solve(self):
		pass


if __name__ == '__main__':
	b = [
		[1, None, 5, None, None, None, None, None, None],
		[None, None, None, 1, None, 3, 5, 6, None],
		[None, 4, None, None, None, None, 2, None, 1],
		[9, None, None, None, 5, None, 7, 3, None],
		[None, 8, None, 3, 1, 4, None, 2, None],
		[None, 3, 6, None, 8, None, None, None, 4],
		[4, None, 1, None, None, None, None, 9, None],
		[None, 7, 2, 8, None, 5, None, None, None],
		[None, None, None, None, None, None, 6, None, 5],
	]
	b2 = [
		[8, None, None, None, 1, None, None, None, 3],
		[None, 4, 7, None, None, None, None, None, None],
		[9, 3, None, None, None, None, None, 4, 8],
		[None, None, None, 4, None, None, 8, None, None],
		[None, 7, None, None, 2, None, None, 5, None],
		[None, 9, None, 5, None, None, None, 2, None],
		[None, 8, None, None, None, 3, None, None, None],
		[None, None, None, None, None, None, 6, None, 7],
		[None, None, 1, None, None, None, 2, 8, 9],
	]
	board = Board(b)
	board.init_status()
	while True:
		nd = board.find_next()
		if nd is not None:
			nd.set_value()
			board.debug()
		else:
			print("Finished!")
			break
	
	pass
