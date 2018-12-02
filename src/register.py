# 英単語の情報をスクレイピング
import requests
import lxml.html
from lib import GoogleImage
from lib import ControlDB

ControlDB.__init__("botDB")

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

print(GoogleImage.getImageURL(words[1][0])[0])

i = 1
for word in words:
    image_url = GoogleImage.getImageURL(word[0])[0]
    sql = "insert into words values (%s, %s, %s, %s, %s, %s, %s)"
    datas = [
        (i, word[0], word[1], 0, 0.0, 0.0, image_url),
    ]
    ControlDB.insert(sql, datas)
    print(i)
    i += 1
