import requests
from bs4 import BeautifulSoup

# load initial webpage of professors
response = requests.get("https://www.bruinwalk.com/search/?category=professors")
try:
    response.raise_for_status()
except Exception as exc:
    print("There was a problem fetching the page: %s" % (exc))

browse = BeautifulSoup(response.text, 'html.parser')

elems = browse.find_all('div', class_='result-card flex-container')
print(type(elems))
print(len(elems))
#print(elems[0])



Donny = elems[0].find('div', 'flex-container professor-meta-content')

Dinfo = Donny.find('a').get('href')
BigD = Donny.find('a', class_= 'professor-name flex-item flex-middle')
print(Dinfo)
print(BigD.text)
