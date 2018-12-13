import requests
import lxml.html
import urllib.parse

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


def Japanese_to_English(japanese):
    url = 'https://ejje.weblio.jp/content/'
    response = requests.get(url + japanese, headers=headers)
    html = lxml.html.fromstring(response.content)
    result = html.xpath('//*[@id="summary"]/div[2]/table/tbody/tr/td[2]/text()')
    print(result)


Japanese_to_English('遊ぶ')
