import os
import sys
import time

import LineApp as LA

if __name__ == '__main__':



    app = LA.LineApp(channel_secret,channel_access_token)

    while True:
        time.sleep(1)
        #print(app.receive)
        app.push_msgs("hello")