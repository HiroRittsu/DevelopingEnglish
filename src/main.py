import datetime
import random
import sys
import time
import re

sys.path.append('../')
from lib import LineApp
from lib import ControlDB
from lib import WeblioTranslate
from lib import JISHO_ORG

userID = 'U444d8a9ca45523b6fcda0226769d9983'

app = LineApp.LineApp(userID)
ControlDB.init('botDB')

DEBUG = False


def getAnswer():
	'''
	:return:
	'''
	start = time.time()
	while len(app.get_msgs()) == 0:
		time.sleep(0.1)
	elapsed_time = time.time() - start
	return app.get_msgs().pop(0)[1], "{0}".format(elapsed_time)


def judge_jp_answer(question, answer):
	'''
	:param question:
	:param answer:
	:return:
	'''
	status = -1
	meanings = JISHO_ORG.Japanese_translation(question)
	answer = JISHO_ORG.fluctuation_correction(answer)  # ゆらぎスペル修正

	for meaning in meanings:
		if meaning == answer:
			status = 1

	return status


def updataUserdata(id, judge, time):
	'''
	:param id:
	:param judge:
	:param time:
	:return:
	'''
	userdata = ControlDB.select('select * from userdata where id =' + str(id))[0]
	answer_count = userdata[1] + 1
	if judge == 1:
		right_rate = userdata[2] + 1
	else:
		right_rate = userdata[2]
	answer_time = time

	ControlDB.update('update userdata set answer_count=' + str(answer_count) + ',right_rate=' + str(
		right_rate) + ',answer_time = ' + str(answer_time) + ' where id=' + str(id))


###########################################################################################

def exam():
	'''
	:return:
	'''
	print("exam!")
	app.push_msgs('英語やりますで')
	app.push_msgs('何か返信!')
	getAnswer()
	question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

	count = 1
	for question_id in question_ids:
		wordset = ControlDB.select(
			'select * from words where id=' + str(question_id[0]))[0]

		app.push_msgs('●問題' + str(count) + '/' + str(len(question_ids)) + '\n  > ' + wordset[1])
		app.push_msgs('回答 🔽')
		answer = getAnswer()

		# カタカナだけの回答は除外
		while not re.compile(r'[\u30A1-\u30F4]+').fullmatch(answer[0]) == None:
			app.push_msgs('カタカナはダメ！！')
			app.push_msgs('回答 🔽')
			answer = getAnswer()

		print(answer[1])

		result = judge_jp_answer(wordset[1], answer[0])

		if result == -1:
			app.push_msgs('不正解　☓')
			app.push_msgs('正解例: ' + wordset[2])
			practice(question_id[0], wordset[1], wordset[2])  # ５回練習
		elif result == 0:
			app.push_msgs('惜しい')
		else:
			app.push_msgs('正解 ❍')

		if not DEBUG:
			updataUserdata(question_id[0], result, answer[1])
		else:
			app.push_msgs('記録はされていません。')

		count += 1

	app.push_msgs('終了')


def practice(id, question, answer):
	app.push_msgs('////////////練習////////////')
	app.push_msgs('5回繰り返しましょう！')
	image = ControlDB.select('select * from image where id=' + str(id))[0][1]
	for i in range(5):
		app.push_img(image)
		flag = True
		while flag:
			app.push_msgs(question + " : " + answer)
			app.push_msgs('🔽')
			practice_answer = getAnswer()
			for a in str(answer).split("、"):
				if a == practice_answer[0]:
					flag = False
				else:
					app.push_msgs('間違っていますヨ')

	app.push_msgs('////////////練習終わり////////////')


##############################################################################


def debug():
	global DEBUG
	app.push_msgs('デバッグモード')
	DEBUG = True
	exam()
	DEBUG = False


def exam_schedule(plans):
	for plan in plans:
		if datetime.datetime.now().hour == plan[0] and datetime.datetime.now().minute == plan[1]:
			exam()
			while datetime.datetime.now().minute == plan[1]:
				time.sleep(1)


def option():
	if not len(app.get_msgs()) == 0:
		option = app.get_msgs().pop(0)[1]
		if option == 'debug':
			print("デバッグモード")
			debug()
		elif option == 'test':
			app.push_msgs('テストモード')
			print("テストモード")
		else:
			app.push_msgs('debug: デバッグモード')
			app.push_msgs('test: テストモード')


############################################################################################

def main():
	while True:
		#exam_schedule([[8, 10], [12, 20], [21, 30]])
		option()
		time.sleep(1)


if __name__ == '__main__':
	main()
