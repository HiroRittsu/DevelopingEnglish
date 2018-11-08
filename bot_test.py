import os
import sys
import time

import LineApp as la

if __name__ == '__main__':

    while True:
        time.sleep(1)
        la.push_msgs("hello")
        print(la.receive)