import sys
from time import sleep

import generate.generate as su


def calculate_region(x, y):
	"""
	to check which region is this point belongs to
	:param x: the x value
	:param y: the y value
	:return: the region number
	"""
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
	"""
	Node is a representation of a single value point in Sudoku
	"""
	
	
	def __init__(self, board, x, y, value=None):
		"""
		to initialize this node with x, y, and the value(default None, which means an empty node)
		:param board: the reference of the board
		:param x: the x value
		:param y: the y value
		:param value: the value of the node
		"""
		# the value of this node
		self._value = value
		# the reference to the Sudoku board
		self._board = board
		# the X value
		self._x = x
		# the Y value
		self._y = y
		# grid number indicate which region this node belongs to (3x3)
		self._grid_number = calculate_region(x, y)
		#
		if self._value is None:
			self._possible = [i for i in range(1, 10)]
		else:
			self._possible = []
		self._notice = False
	
	
	def is_noticed(self):
		"""
		:return: True if notice is called, False otherwise
		"""
		return self._notice
	
	
	def notice(self):
		"""
		:return: notice this node
		"""
		self._notice = True
	
	
	def discard_notice(self):
		"""
		:return: discard the notice
		"""
		self._notice = False
	
	
	def reduce_possible(self, value):
		"""
		To reduce a possible value from this node, used when other node is set
		:param value: the value need to be reduced
		"""
		if not self.is_set() and value in self._possible:
			self._possible.remove(value)
	
	
	def is_set(self):
		"""
		indicate this node is set to a value or not
		:return: True if this node is set, False otherwise
		"""
		return self._value is not None
	
	
	def set_value(self, value):
		"""
		used when a value is set, this method automatically call the Board.refresh to reduce the related node's possible
		:param value: the value set to this node
		"""
		self.reduce_possible(value)
		self._value = value
		self._board.refresh(self)
	
	
	def possible(self):
		"""
		:return: The possible value of this node
		"""
		return self._possible
	
	
	def possible_size(self):
		"""
		:return: The size of the possible value
		"""
		return self._possible.__len__()
	
	
	def value(self):
		"""
		:return: the value of this node
		"""
		return self._value
	
	
	def x(self):
		"""
		:return: the X value
		"""
		return self._x
	
	
	def y(self):
		"""
		:return: the Y lue
		"""
		return self._y
	
	
	def grid_number(self):
		"""
		:return: the grid number which indicate which region this node belongs to
		"""
		return self._grid_number
	
	
	def restore(self, value_node):
		"""
		to restore the status of this node
		:param value_node: the node value that was recorded
		"""
		self._value = value_node[1]
		self._possible = value_node[2]
	
	
	def __repr__(self):
		return "({}, {}, value={}, possible={})".format(self._x, self._y, self._value, self._possible)
	
	
	def __str__(self):
		return self.__repr__()


class Board:
	"""
	Board is a representation of the actually Suduko board
	"""
	
	
	def __init__(self, board):
		"""
		to init the board, including all the board in the node and the grid
		:param board: the init state of the board
		"""
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
		self._init_status()
	
	
	def refresh(self, n):
		"""
		to reduce possible in the x, y, grid, direction
		:param n: the node which is operating on
		"""
		self._refresh_x(n)
		self._refresh_y(n)
		self._refresh_grid(n)
	
	
	def _refresh_x(self, n):
		"""
		to refresh all the node which has the same x value
		:param n: the node which is operating on
		"""
		l_x = [line[n.x()] for line in self._board]
		for c_node in l_x:
			if c_node == n:
				continue
			c_node.reduce_possible(n.value())
	
	
	def _refresh_y(self, n):
		"""
		to refresh all the node which has the same y value
		:param n: the node which is operating on
		"""
		l_y = self._board[n.y()]
		for c_node in l_y:
			if c_node == n:
				continue
			c_node.reduce_possible(n.value())
	
	
	def _refresh_grid(self, n):
		"""
		to refresh all the node which has the same grid number
		:param n: the node which is operating on
		"""
		l_grid = self._grids[n.grid_number()]
		for c_node in l_grid:
			if c_node == n:
				continue
			c_node.reduce_possible(n.value())
	
	
	def _record(self):
		"""
		:return: to save a record of the current board
		"""
		return [(node, node.value(), [i for i in node.possible()]) for line in self._board for node in line]
	
	
	def _restore(self, recovery):
		"""
		to restore a record from a recovery
		:param recovery: the recovery that has been recoded
		"""
		for record in recovery:
			record[0].restore(record)
	
	
	def _init_status(self):
		"""
		to initialize the board since all the node default has [1~9] as it's possible
		"""
		for line in self._board:
			for node in line:
				if not node.is_set():
					continue
				self.refresh(node)
	
	
	def print_sudoku(self, file=sys.stdout):
		"""
		print the current representation of the board
		:param file: the file output stream that wants to be printed on
		"""
		real_index = 0
		for x in range(13):
			for y in range(13):
				if x % 4 == 0:
					if y % 4 == 0:
						print("+", end="", file=file)
					else:
						print("---", end="", file=file)
				else:
					if y % 4 == 0:
						print("|", end="", file=file)
					else:
						node = self._board[real_index % 9][real_index // 9]
						value = node.value()
						if node.is_noticed():
							node.discard_notice()
							if value is None:
								print("( )", end="", file=file)
							else:
								print("(" + str(value) + ")", end="", file=file)
						else:
							if value is None:
								print("   ", end="", file=file)
							else:
								print(" " + str(value) + " ", end="", file=file)
						real_index += 1
			print("\n", end="", file=file)
	
	
	def _find_next(self):
		"""
		find all node that hasn't been set a value and sort them by the size of their possibility
		:return: the node list
		"""
		node_list = [node for line in self._board for node in line if not node.is_set()]
		node_list.sort(key=lambda node: node.possible_size())
		return node_list
	
	
	def _is_finished(self):
		"""
		:return: True of all the value in the board has been set, False otherwise
		"""
		return all([node.is_set() for line in self._board for node in line])
	
	
	def solve(self):
		"""
		to attempt to solve this Suduko
		"""
		result = self._attempt(self._find_next())
		sleep(0.1)
		print("Successful!" if result else "UnSuccessful!", file=sys.stderr)
		self.print_sudoku(sys.stderr)
	
	
	def _attempt(self, node_list):
		"""
		attempting solving this current Suduko
		:param node_list: the node list
		:return: Ture if success, False otherwise
		"""
		# print this sudoku
		self.print_sudoku()
		# iterate all the node in node list
		for node in node_list:
			# copy a reference of the possible
			possible = [i for i in node.possible()]
			# if no possible value can be set to this node, return
			if possible.__len__() == 0:
				break
			else:
				# iterate through all the possible value and try them all
				for value in possible:
					# to restore the current statue
					recovery = self._record()
					# set the value
					node.set_value(value)
					# notice this node, since there is operation performed on it (style use)
					node.notice()
					# if the board is finished return True
					if self._is_finished():
						return True
					else:
						# if not attempt to the next level
						# if not success, restore the current recovery and try anther value or the next node
						if self._attempt(self._find_next()):
							return True
						else:
							# restore the recovery
							self._restore(recovery)
		# fail return false
		return False


if __name__ == '__main__':
	# b = [
	# 	[8, None, None, None, 1, None, None, None, 3],
	# 	[None, 4, 7, None, None, None, None, None, None],
	# 	[9, 3, None, None, None, None, None, 4, 8],
	# 	[None, None, None, 4, None, None, 8, None, None],
	# 	[None, 7, None, None, 2, None, None, 5, None],
	# 	[None, 9, None, 5, None, None, None, 2, None],
	# 	[None, 8, None, None, None, 3, None, None, None],
	# 	[None, None, None, None, None, None, 6, None, 7],
	# 	[None, None, 1, None, None, None, 2, 8, 9],
	# ]
	b = su.kou(su.make_board())
	# b = [
	# 	[1, None, 5, None, None, None, None, None, None],
	# 	[None, None, None, 1, None, 3, 5, 6, None],
	# 	[None, 4, None, None, None, None, 2, None, 1],
	# 	[9, None, None, None, 5, None, 7, 3, None],
	# 	[None, 8, None, 3, 1, 4, None, 2, None],
	# 	[None, 3, 6, None, 8, None, None, None, 4],
	# 	[4, None, 1, None, None, None, None, 9, None],
	# 	[None, 7, 2, 8, None, 5, None, None, None],
	# 	[None, None, None, None, None, None, 6, None, 5],
	# ]
	# b = [
	# 	[2, 8, 4, 7, 5, 9, 1, 6, 3],
	# 	[6, 1, 7, 8, 3, 2, 5, 9, 4],
	# 	[3, 9, 5, 4, 6, 1, 2, 7, None],
	# 	[8, 5, 6, 2, 9, 4, 7, None, 1],
	# 	[7, 4, 3, 1, 8, 5, None, 2, 9],
	# 	[1, 2, 9, 3, 7, 6, 8, 4, 5],
	# 	[4, 7, 8, 6, 1, 3, 9, 5, 2],
	# 	[9, 6, 2, 5, 4, 8, 3, 1, 7],
	# 	[5, 3, 1, 9, 2, 7, 4, 8, 6]
	# ]
	sudoku = Board(b)
	sudoku.print_sudoku()
	input()
	sudoku.solve()
