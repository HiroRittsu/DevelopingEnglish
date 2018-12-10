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


def answer():
    while len(app.get_msgs()) == 0:
        print('wait')
        time.sleep(0.1)
    return app.get_msgs().pop(0)[1]


def job():
    print("job!")
    app.push_msgs(userID, 'start')
    question_ids = random.sample(ControlDB.select('select id from userdata'), 5)

    for question_id in question_ids:
        question = str(ControlDB.select(
            'select * from words where id=' + str(question_id).replace(',)', '').replace('(', ''))).split(',')

        app.push_msgs(userID, question[1])

        print(answer())


schedule.every(10).seconds.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
