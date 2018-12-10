import random
import sys
import time

import schedule

sys.path.append('../lib/')
import LineApp
import ControlDB

app = LineApp.LineApp()
ControlDB.init('botDB')

userID = 'U444d8a9ca45523b6fcda0226769d9983'


def getAnswer():
    while len(app.get_msgs()) == 0:
        time.sleep(0.1)
    return app.get_msgs().pop(0)[1]


def judgeAnswer(input, right_answers):
    status = -1
    for a in right_answers.split('、'):
        print(a.replace(')]', '').replace('\'', '').replace(' ', ''))
        if input in a:
            status = 0
        if a.replace(')]', '').replace('\'', '').replace(' ', '') == input:
            status = 1

    return status


def job():
    print("job!")
    app.push_msgs(userID, 'start')
    question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

    count = 1
    for question_id in question_ids:
        print(question_id[0])
        question = ControlDB.select(
            'select * from words where id=' + str(question_id[0][0]))[0]

        print(question)

        app.push_msgs(userID, '●問題' + str(count) + '/5\n  > ' + question[1].replace('\'', ''))
        print(question[2])

        answer = getAnswer()

        result = judgeAnswer(answer, question[2])

        if result == -1:
            app.push_msgs(userID, '不正解')
        elif result == 0:
            app.push_msgs(userID, '惜しい')
        else:
            app.push_msgs(userID, '正解')

        count += 1

    app.push_msgs(userID, '終了')


schedule.every(1).seconds.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
