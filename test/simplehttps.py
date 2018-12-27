import requests
import lxml.html

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


def Japanese_to_English(japanese):
    results = set()
    url = 'https://thesaurus.weblio.jp/content/%E6%80%9D%E3%81%84%E3%82%84%E3%82%8B'
    response = requests.get(url, headers=headers)
    html = lxml.html.fromstring(response.content)

    gets = html.xpath('//*[@id="main"]/div[3]/div/div[1]/table/tr/td/a/text()')
    gets = html.xpath('//*[@id="main"]/div[5]/div/div[1]/table/tr/td[2]/following()')
    print(gets)


Japanese_to_English('')
