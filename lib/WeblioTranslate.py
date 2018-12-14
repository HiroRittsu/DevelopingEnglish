import requests
import lxml.html

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


def Japanese_to_English(japanese):
    results = set([])
    url = 'https://ejje.weblio.jp/content/'
    response = requests.get(url + japanese, headers=headers)
    html = lxml.html.fromstring(response.content)

    # もしかして候補
    candidate = html.xpath('//*[@id="main"]/div[2]/div[2]/div/div[1]/div/a/@href')
    if not len(candidate) == 0:
        response = requests.get(candidate[0], headers=headers)
        html = lxml.html.fromstring(response.content)

    # 主な英訳
    gets = html.xpath('//*[@id="summary"]/div[2]/table/tbody/tr/td[2]/text()')
    if not len(gets) == 0:
        if '、' in gets[0]:
            for r in str(gets[0]).split('、'):
                results.add(r)
        else:
            for r in str(gets[0]).split(' '):
                results.add(r.replace(';', ''))

    gets = html.xpath('//*[@id="hideDictPrsKENJE"]/div[1]/div[1]/div[2]/div/div[1]/p[2]/a/text()')
    if len(gets) == 0:
        gets = html.xpath('//*[@id="hideDictPrsKENJE"]/div[1]/div[1]/div[2]/div/div[1]/table/tr/td[2]/a/text()')

    for r in gets:
        results.add(r)

    print(results)