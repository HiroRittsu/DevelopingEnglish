import csv

DATA_BASE_DIR = '../data/'


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


def main():
	words = []
	with open(DATA_BASE_DIR + 'wordtest_1.csv', 'r') as f:
		reader = csv.reader(f)

		for row in reader:
			words.append(row)

	print(words)
	print(question_sentence(words[3][0], words[3][1]))


if __name__ == '__main__':
	main()
