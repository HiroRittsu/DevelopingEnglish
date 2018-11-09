import time
import LineApp as la

id = ''

if __name__ == '__main__':

    app = la.LineApp()

    while True:
        time.sleep(1)
        msg = app.get_msgs()

        if not msg == '':
            id = msg[0]

        if not id == '':
            app.push_msgs(id,'hello')