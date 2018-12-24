import sys

sys.path.append('../lib/')
import ControlDB

import random

ControlDB.init('botDB')

# print(len(ControlDB.select('select id from userdata')))

# print(str(random.sample(ControlDB.select('select id from userdata'), 10)[0]).replace(',)', '').replace('(', ''))

# ControlDB.update('update userdata set answer_count=1,right_rate=2 where id=2')
# array = np.asarray([])
# array = np.append(array, ControlDB.select('select id from userdata')[0])
print()
# print(random.sample(ControlDB.select('select id from userdata'), 5)[0][0])

print(ControlDB.select('select * from userdata where id = 2')[0])

ControlDB.update('update userdata set answer_count=10,right_rate=1 where id=2')
