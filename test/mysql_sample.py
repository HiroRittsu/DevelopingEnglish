import sys

sys.path.append('../lib/')
import ControlDB
import random

ControlDB.init('botDB')

# print(len(ControlDB.select('select id from userdata')))

# print(str(random.sample(ControlDB.select('select id from userdata'), 10)[0]).replace(',)', '').replace('(', ''))

ControlDB.update('update userdata set answer_count=1,right_rate=2 where id=2')
