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
    flag = False
    for a in right_answers.split('、'):
        print(a.replace(')]', '').replace('\'', '').replace(' ', ''))
        if a.replace(')]', '').replace('\'', '').replace(' ', '') == input:
            flag = True
    return flag


def job():
    print("job!")
    app.push_msgs(userID, 'start')
    question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

    for question_id in question_ids:
        question = str(ControlDB.select(
            'select * from words where id=' + str(question_id).replace(',)', '').replace('(', ''))).split(',')

        app.push_msgs(userID, question[1].replace('\'', ''))

        answer = getAnswer()

        print(answer)
        print(judgeAnswer(answer, question[2]))


schedule.every(10).seconds.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
