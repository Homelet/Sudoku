import itertools
import random
from copy import deepcopy


# 创建3*3的区块
def make_board(m=3):
	numbers = list(range(1, m ** 2 + 1))  # 创建（1 ~ 9）的列表
	board = None  # board是数独二维列表
	
	while board is None:
		board = attempt_board(m, numbers)
	return board


def attempt_board(m, numbers):
	n = m ** 2
	
	board = [[None for _ in range(n)] for _ in range(n)]
	
	for i, j in itertools.product(range(n), repeat=2):
		i0, j0 = i - i % m, j - j % m  # i，j 分别代表行和列。 i0和j0分别代表起始位置
		random.shuffle(numbers)
		for x in numbers:  # 检查行，列，区域
			if x not in board[i] and all(row[j] != x for row in board) and all(
					x not in row[j0:j0 + m] for row in board[i0:i]):
				board[i][j] = x  # 过检赋值
				break
		else:
			return None
	return board


def kou(board, m=3):
	numbers = list(range(1, m ** 2 + 1))
	omit = 5  # 难度控制 omit代表随机把每一行抹去几个数字
	challange = deepcopy(board)
	for i, j in itertools.product(range(omit), range(m ** 2)):
		x = random.choice(numbers) - 1
		challange[x][j] = None
	return challange
