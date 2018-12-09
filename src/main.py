import sys
import time

import schedule

sys.path.append('../lib/')
import LineApp
from lib import ControlDB

app = LineApp.LineApp()

userID = 'U444d8a9ca45523b6fcda0226769d9983'


def job():
    print("job!")
    app.push_msgs(userID, 'start')



schedule.every(10).seconds.do(job)


def main():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
