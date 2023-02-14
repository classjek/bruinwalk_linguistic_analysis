import requests
from bs4 import BeautifulSoup

class Professor:
    def __init__(self, name):
        self.name = name
        self.classes = []

class Review:
    def __init__(self, name):
        self.name = name
        self.grade = 0
        self.text = ""

# given an href for a class, this function will return a list of 
def grab_classes(href, name):
    # load the web page 
    response = requests.get(web_add + href)
    try:
        response.raise_for_status()
    except Exception as exc:
        print("There was a problem fetching a class page: %s" % (exc))

    # get every review in a list called reviews 
    class_page = BeautifulSoup(response.text, 'html.parser')
    reviews_block = class_page.find('div', 'reviews row')
    reviews = reviews_block.find_all('div', 'review reviewcard')

    # for each review, create a review object containing
    # the grade, title, and text of the review 
    for _ in reviews: 
        temp_review = Review(name)
        #print(type(_))
        text = _.find('div', class_='grade-margin')
        #print(type(text), text.text)
        text = _.find('div', class_='expand-area review-paragraph')
        paragraph = text.find('p')
        print(paragraph.text)





# load initial webpage of professors
response = requests.get("https://www.bruinwalk.com/search/?category=professors")
try:
    response.raise_for_status()
except Exception as exc:
    print("There was a problem fetching the page: %s" % (exc))

# load intial webpage with all professors, extract each one onto a page
browse = BeautifulSoup(response.text, 'html.parser')
elems = browse.find_all('div', class_='result-card flex-container')


web_add = 'https://www.bruinwalk.com'

prof = elems[0].find('div', 'flex-container professor-meta-content')


# will put into large for loop, right now loops through one professor 
phref = prof.find('a').get('href')
p1 = Professor(prof.find('a', class_= 'professor-name flex-item flex-middle').text)
print(p1.name)


# load professor's individual web page 
prof_page = requests.get(web_add + phref)
try:
    prof_page.raise_for_status()
except Exception as exc:
    print('There was a problem loading a professor\'s page: %s' % (exc))

browse = BeautifulSoup(prof_page.text, 'html.parser')

# grab each of the professors classes as an element
classes = browse.find_all('div', 'title-container')

# tbc
"""
for c in classes:
    grab_classes(c.find('a').get('href'))
"""

grab_classes("/professors/stephen-j-dickey/engl-90/", 'Stephen Dickey')




