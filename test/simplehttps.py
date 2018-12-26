import requests
import lxml.html

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


def Japanese_to_English(japanese):
    results = set()
    url = 'https://jisho.org/search/protection'
    response = requests.get(url, headers=headers)
    html = lxml.html.fromstring(response.content)

    gets = html.xpath('//*[@id="primary"]/div[1]/div/div[1]/div[2]/ul[1]/li[1]/a/text()')
    for g in gets:
        results.add(str(g).replace("Sentence search for ", ""))
    gets = html.xpath('//*[@id="primary"]/div/div/div/ul[1]/li[1]/a/text()')
    for g in gets:
        results.add(str(g).replace("Sentence search for ", ""))
    print(results)


Japanese_to_English('')
