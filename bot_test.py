import time
import LineApp as la

if __name__ == '__main__':

    app = la.LineApp()
    msg = []
    id = ''

    while True:
        time.sleep(1)
        msg = app.get_msgs()

        if not len(msg) == 0:
            id = msg[0]

        if not id == '':
            app.push_msgs(id,'hello')