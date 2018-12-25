import datetime
import random
import sys
import time
import re

sys.path.append('../lib/')
import LineApp
import ControlDB
import WeblioTranslate

app = LineApp.LineApp()
ControlDB.init('botDB')

userID = 'U444d8a9ca45523b6fcda0226769d9983'

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


def judgeAnswer(question, answer):
    '''
    :param question:
    :param answer_en:
    :return:
    '''
    status = -1
    for a in WeblioTranslate.Japanese_to_English(answer):
        if a == question[1]:
            status = 1
    for q in str(question[2]).split("、"):
        print(q)

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
    app.push_msgs(userID, '英語やりますで')
    app.push_msgs(userID, '何か返信!')
    getAnswer()
    question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

    count = 1
    for question_id in question_ids:
        question = ControlDB.select(
            'select * from words where id=' + str(question_id[0]))[0]

        app.push_msgs(userID, '●問題' + str(count) + '/' + str(len(question_ids)) + '\n  > ' + question[1])
        app.push_msgs(userID, '回答 🔽')
        answer = getAnswer()

        # カタカナだけの回答は除外
        while not re.compile(r'[\u30A1-\u30F4]+').fullmatch(answer[0]) == None:
            app.push_msgs(userID, 'カタカナはダメ！！')
            app.push_msgs(userID, '回答 🔽')
            answer = getAnswer()

        print(answer[1])

        result = judgeAnswer(question, answer[0])

        if result == -1:
            app.push_msgs(userID, '不正解　☓')
            app.push_msgs(userID, '正解例: ' + question[2])
            practice(question_id[0], question[1], question[2])  # ５回練習
        elif result == 0:
            app.push_msgs(userID, '惜しい')
        else:
            app.push_msgs(userID, '正解 ❍')

        if not DEBUG:
            updataUserdata(question_id[0], result, answer[1])
        else:
            app.push_msgs(userID, '記録はされていません。')

        count += 1

    app.push_msgs(userID, '終了')


def practice(id, question, answer):
    app.push_msgs(userID, '//////練習//////')
    app.push_msgs(userID, '5回繰り返しましょう！')
    image = ControlDB.select('select * from image where id=' + str(id))[0][1]
    for i in range(5):
        app.push_img(userID, image)
        app.push_msgs(userID, question + " : " + answer)
        app.push_msgs(userID, '🔽')
        getAnswer()

    ##############################################################################


def debug():
    global DEBUG
    app.push_msgs(userID, 'デバッグモード')
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
            app.push_msgs(userID, 'テストモード')
            print("テストモード")
        else:
            app.push_msgs(userID, 'debug: デバッグモード')
            app.push_msgs(userID, 'test: テストモード')


############################################################################################

def main():
    while True:
        exam_schedule([[8, 10], [12, 20], [21, 30]])
        option()
        time.sleep(1)


if __name__ == '__main__':
    main()
