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


def job():
    print("job!")
    app.push_msgs(userID, 'start')
    question_ids = random.sample(ControlDB.select('select id from userdata'), 10)

    for question_id in question_ids:
        print(ControlDB.select('select * from words where id=', str(question_id).replace(',)', '').replace('(', ''))
              )


schedule.every(10).seconds.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
