import time
import sys, os

sys.path.append('../lib/')
import LineApp as la

if __name__ == '__main__':

    app = la.LineApp()
    msg = []
    id = ''
    while True:
        time.sleep(1)
        # msg = app.get_msgs()

        if not len(app.get_msgs()) == 0:
            print(app.get_msgs().pop(0))
            print(app.get_msgs().remove(0))

        # app.push_msgs('U444d8a9ca45523b6fcda0226769d9983', '尊い...っっ!!')

        # app.push_img('U444d8a9ca45523b6fcda0226769d9983', 'https://cdn.ibispaint.com/movie/372/896/372896921/image372896921.png')
