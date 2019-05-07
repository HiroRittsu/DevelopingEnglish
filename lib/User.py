class User:
	def __init__(self, id: str, ex_function):
		self.id = id
		# 問題と答えを辞書に格納
		self.q = {}
