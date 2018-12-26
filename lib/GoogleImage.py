from urllib import request as req
from urllib import parse
import bs4


def getImageURL(keyword):
    image_links = []

    urlKeyword = parse.quote(keyword)
    url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
    request = req.Request(url=url, headers=headers)
    page = req.urlopen(request)

    html = page.read().decode('utf-8')
    html = bs4.BeautifulSoup(html, "html.parser")
    elements = html.select('.rg_meta.notranslate')

    for element in elements:
        for e in str(element).split(","):
            if "http" in e and "\"ou\"" in e:
                image_links.append(e.replace("\"", "").replace("ou:", ""))

    for link in image_links:
        if str(link)[-4:] == '.jpg' or str(link)[-4:] == '.png':
            if 'https://' in link:
                return link

    return 'https://www.suzuran-dc.com/wp-content/uploads/non-image.jpg'
