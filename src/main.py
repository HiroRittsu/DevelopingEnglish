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


def getAnswer():
    '''
    :return:
    '''
    start = time.time()
    while len(app.get_msgs()) == 0:
        time.sleep(0.1)
    elapsed_time = time.time() - start
    return app.get_msgs().pop(0)[1], "{0}".format(elapsed_time)


def judgeAnswer(question, answer_en):
    '''
    :param question:
    :param answer_en:
    :return:
    '''
    status = -1
    for a in answer_en:
        print(a)
        if a == question:
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

def job():
    '''
    :return:
    '''
    print("job!")
    app.push_msgs(userID, '英語やりますで')
    app.push_msgs(userID, '何か返信!')
    getAnswer()
    question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

    count = 1
    for question_id in question_ids:
        question = ControlDB.select(
            'select * from words where id=' + str(question_id[0]))[0]

        app.push_msgs(userID, '●問題' + str(count) + '/5\n  > ' + question[1])
        app.push_msgs(userID, '回答 🔽')
        answer = getAnswer()

        # カタカナだけの回答は除外
        while not re.compile(r'[\u30A1-\u30F4]+').fullmatch(answer[0]) == None:
            app.push_msgs(userID, 'カタカナはダメ！！')
            app.push_msgs(userID, '回答 🔽')
            answer = getAnswer()

        print(answer[1])

        result = judgeAnswer(question[1], WeblioTranslate.Japanese_to_English(answer[0]))

        if result == -1:
            app.push_msgs(userID, '不正解　☓')
            app.push_msgs(userID, '正解例: ' + question[2])
        elif result == 0:
            app.push_msgs(userID, '惜しい')
        else:
            app.push_msgs(userID, '正解 ❍')

        updataUserdata(question_id[0], result, answer[1])

        count += 1

    app.push_msgs(userID, '終了')


##############################################################################

def schedule(plans):
    for plan in plans:
        if datetime.datetime.now().hour == plan[0] and datetime.datetime.now().minute == plan[1]:
            job()
            while datetime.datetime.now().minute == plan[1]:
                time.sleep(1)


def option():
    if not len(app.get_msgs()) == 0:
        option = app.get_msgs().pop(0)[1]
        if option == 'debug':
            app.push_msgs(userID, 'デバッグモード')
            print("デバッグモード")
        if option == 'test':
            app.push_msgs(userID, 'テストモード')
            print("テストモード")
        else:
            app.push_msgs(userID, 'debug: デバッグモード')
            app.push_msgs(userID, 'test: テストモード')


############################################################################################

def main():
    while True:
        schedule([[0, 2], [23, 47]])
        option()
        time.sleep(1)


if __name__ == '__main__':
    main()
