import time
import sys,os
sys.path.append('./lib/')
import LineApp as la

if __name__ == '__main__':

    app = la.LineApp()
    msg = []
    id = ''

    while True:
        time.sleep(1)
        # msg = app.get_msgs()

        print(app.get_msgs())

        app.push_msgs('U444d8a9ca45523b6fcda0226769d9983', 'hello')

        app.push_img('U444d8a9ca45523b6fcda0226769d9983', 'https://597e077e.ngrok.io/')