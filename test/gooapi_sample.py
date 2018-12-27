import requests

headers = {
    'Content-type': 'application/json',
}
text1 = '猫は元気だ。'
text2 = '彼は嘘を付いている'
data = '{"app_id":"a9406a7771ebd284669a62f66e3a711e2e1335ac9822db3f650f24ad3cde9663", "text1":"' + text1 + '", "text2":"' + text2 + '"}'
data = data.encode('utf-8')
response = requests.post('https://labs.goo.ne.jp/api/textpair', headers=headers, data=data)
print(float(response.json()['score']))
