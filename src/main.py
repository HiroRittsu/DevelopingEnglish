import csv
import random
from googletrans import Translator

DATA_BASE_DIR = '../data/'


def get_words():
	'''
	csvから読み取り
	:return:
	'''
	words = []
	with open(DATA_BASE_DIR + 'wordtest_1.csv', 'r') as f:
		reader = csv.reader(f)

		for row in reader:
			words.append(row)
	return words


def question_sentence(row_word: str, row_sentence: str):
	'''
	虫食いにする
	:param row_word:
	:param row_sentence:
	:return:
	'''
	word_list = row_sentence.split(' ')
	for i in range(len(word_list)):
		if row_word == word_list[i][:len(row_word)]:
			return word_list[i], row_sentence.replace(word_list[i], '_' * len(word_list[i]))


def get_word_group(words: list, answer: str, count: int):
	example_words = []
	for i in range(len(words)):
		example_words.append(words[i][0])
	selected = random.sample(example_words, k=count)

	# 答えが含まれていない場合
	if not answer in selected:
		selected.pop()
		selected.append(answer)
		selected = random.sample(selected, k=len(selected))

	result = ''
	for i in range(len(selected)):
		result += selected[i] + ' , '
	return '[ ' + result[0:-3] + ' ]'


def judge(input: str, answer: str, translator: Translator):
	if input == answer:
		print("正解", '(' + translator.translate(answer, dest='ja').text + ')')
	else:
		print("不正解:", answer, '(' + translator.translate(answer, dest='ja').text + ')')


def main():
	original_words = get_words()
	words = random.sample(original_words, k=len(original_words))
	translator = Translator()

	for i in range(len(words)):
		answer, question = question_sentence(words[i][0], words[i][1])
		print(i + 1, ': ' + question)
		print(get_word_group(words, words[i][0], 3))
		judge(input(), answer, translator)
		print("")


if __name__ == '__main__':
	main()
