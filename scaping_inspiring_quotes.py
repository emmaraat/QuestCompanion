from bs4 import BeautifulSoup
import urllib.request,urllib.parse,urllib.error
import ssl

ctx=ssl.create_default_context()
ctx.check_hostnanme= False
ctx.verify_mode=ssl.CERT_NONE

url = urllib.request.Request('https://wisdomquotes.com/famous-quotes/',headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(url,context= ctx).read()
soup = BeautifulSoup(response,'html.parser')
#print(soup.prettify())

#d=soup.find('div',attrs={"class": 'entry-content'})
a = soup.find_all('blockquote')
quotes =[]
for i in a:
    item = i.text
    if item.endswith('Click to tweet'):
        item = item[:-15]
    #last_i = item.rfind('.')
    #news = item[:last_i] + "--" + item[last_i+2:]
    #quote,author = 
    quotes.append(item)
    #print(i.text)
with open('quotes_dataset.txt', 'w') as f:
    for item in quotes:
        f.write("%s\n" % item)