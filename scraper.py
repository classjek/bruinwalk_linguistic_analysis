import requests
from bs4 import BeautifulSoup

# load initial webpage of professors
response = requests.get("https://www.bruinwalk.com/search/?category=professors")
#response = requests.get("https://letterboxd.com/jekon13/films/reviews/by/activity/")
try:
    response.raise_for_status()
except Exception as exc:
    print("There was a problem fetching the page: %s" % (exc))

browse = BeautifulSoup(response.text, 'html.parser')

elems = browse.find_all('div', class_='results')
print(type(elems))
print(len(elems))
#print(elems[0])

teachers = elems[0].find_all('div', class_='result-card flex-container')
print(len(teachers))