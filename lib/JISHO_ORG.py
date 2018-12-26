import requests
import lxml.html

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


def Japanese_translation(english):
    results = set()
    url = 'https://jisho.org/search/'
    response = requests.get(url + english, headers=headers)
    html = lxml.html.fromstring(response.content)

    gets = html.xpath('//*[@id="primary"]/div[1]/div/div[1]/div[2]/ul[1]/li[1]/a/text()')
    for g in gets:
        results.add(str(g).replace("Sentence search for ", ""))
    gets = html.xpath('//*[@id="primary"]/div/div/div/ul[1]/li[1]/a/text()')
    for g in gets:
        results.add(str(g).replace("Sentence search for ", ""))

    return results


def fluctuation_correction(japanese):
    url = 'https://jisho.org/search/'
    response = requests.get(url + japanese, headers=headers)
    html = lxml.html.fromstring(response.content)

    gets = html.xpath('//*[@id="primary"]/div/div[1]/div[1]/div[2]/ul/li[1]/a/text()')

    return gets[0].replace("Sentence search for ", "")


print(fluctuation_correction('ぎょうさん'))
print(Japanese_translation('meaning'))
