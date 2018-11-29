# 英単語の情報をスクレイピング
import requests
import lxml.html

urls = []
urls.append('http://www.eigo-duke.com/tango/TOEIC1-300.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC301-600.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC901-1200.html')
urls.append('http://www.eigo-duke.com/tango/TOEIC1201-1500.html')


# urls.append('http://www.eigo-duke.com/tango/TOEICjukugo.html')

def getWords(words,url):
    response = requests.get(url)
    html = lxml.html.fromstring(response.content)

    for i in range(2, 302):
        english = html.xpath('/html/body/table/tbody/tr[4]/td[1]/table[3]/tbody/tr['+ str(i) + ']/td[2]/font/text()')
        japanese = html.xpath('/html/body/table/tbody/tr[4]/td[1]/table[3]/tbody/tr['+ str(i) + ']/td[3]/font/text()')
        if not len(english) == 0 and not len(japanese) == 0:
            print(english[0],japanese[0])
            words.append([english[0],japanese[0]])


words = []
for page in urls:
    print(page)
    getWords(words,page)


