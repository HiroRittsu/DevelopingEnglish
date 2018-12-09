# 英単語の情報をスクレイピング
import sys

import requests
import lxml.html

sys.path.append('../lib/')
import GoogleImage
import ControlDB

ControlDB.init("botDB")

urls = []
urls.append('http://www.eigo-duke.com/tango/TOEIC1-300.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC301-600.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC901-1200.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC1201-1500.html')


# urls.append('http://www.eigo-duke.com/tango/TOEICjukugo.html')

def getWords(words, url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.content)

    for i in range(2, 302):
        english = html.xpath('/html/body/table/tbody/tr[4]/td[1]/table[3]/tbody/tr[' + str(i) + ']/td[2]/font/text()')
        japanese = html.xpath('/html/body/table/tbody/tr[4]/td[1]/table[3]/tbody/tr[' + str(i) + ']/td[3]/font/text()')
        if not len(english) == 0 and not len(japanese) == 0:
            words.append([english[0], japanese[0]])


words = []
for page in urls:
    getWords(words, page)

print(words)

print(GoogleImage.getImageURL(words[1][0]))

i = 1
for word in words:
    image_url = GoogleImage.getImageURL(word[0])
    words_sql = "insert into words values (%s, %s, %s)"
    image_sql = "insert into image values (%s, %s)"
    userdata_sql = "insert into userdata values (%s, %s, %s, %s)"
    datas = [
        (i, word[0], word[1]),
        (i, image_url),
        (i, 0, 0.0, 0.0)
    ]

    ControlDB.insert(words_sql, datas[0])
    ControlDB.insert(image_sql, datas[1])
    ControlDB.insert(userdata_sql, datas[2])
    print(i)
    i += 1
