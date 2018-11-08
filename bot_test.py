import os
import sys
import time

import LineApp as LA

if __name__ == '__main__':

    # get channel_secret and channel_access_token from your environment variable
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
    if channel_secret is None:
        print('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)

    app = LA.LineApp(channel_secret,channel_access_token)

    while True:
        time.sleep(1)
        print(app.receive)