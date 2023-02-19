import requests
from bs4 import BeautifulSoup

# each professor will have a list of reviews under their name
# this is so we can easily test with different control variables without having to sort through every review 
class Professor:
    def __init__(self, name):
        self.name = name
        self.classes = []

class Class:
    def __init__(self, name, href):
        self.name = name
        self.href = href

class Review:
    def __init__(self, name):
        self.name = name
        self.grade = ""
        self.text = ""

# grades are held in a wierd text with lots of extra space so this will clean them up
# this could definitely be optimized but this program will only run once so who cares
def get_grade(raw_grade):
    if(raw_grade.find('N/A') != -1):
        return('N/A')
    elif(raw_grade.find('A') != -1):
        if(raw_grade.find('A-') != -1):
            return('A-')
        elif(raw_grade.find('A+') != -1):
            return('A+')
        else:
            return('A')  
    elif(raw_grade.find('B') != -1):
        if(raw_grade.find('B-') != -1):
            return('B-')
        elif(raw_grade.find('B+') != -1):
            return('B+')
        else:
            return('B')
    elif(raw_grade.find('C') != -1):
        if(raw_grade.find('C-') != -1):
            return('C-')
        elif(raw_grade.find('C+') != -1):
            return('C+')
        else:
            return('C')
    elif(raw_grade.find('D') != -1):
        if(raw_grade.find('D-') != -1):
            return('D-')
        elif(raw_grade.find('D+') != -1):
            return('D+')
        else:
            return('D')
    else:
        return('F')

# Given the href of a class, this will grab every review from that class 
# maybe load the page here and then pass it through as a parameter?
def through_class(href):
    val = grab_classes(href, 'dummyName')

    bruh = 0
    while val != 0:
        grab_classes(val, 'dummyName')
        bruh +=1
        if bruh > 5:
            break



# make this return 0 or the href of the next page 
# given an href for a page of reviews, this will grab the text and grade from each review and return a list of them 
def grab_classes(href, prof_name):

    #print(prof_name.name)
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


    #eventually make this a class object and have that class belong to the prof
    teach = []

    print('Grabbing shit from', href)

    """
    # for each review, create a review object containing
    # the grade, title, and text of the review 
    for _ in reviews: 
        temp_review = Review(prof_name.name)
        #print(type(_))
        text = _.find('div', class_='grade-margin')
        temp_review.grade = get_grade(text.text)

        #print(type(text), text.text)
        text = _.find('div', class_='expand-area review-paragraph')
        paragraph = text.find('p')

        temp_review.text = paragraph.text
        #print(paragraph.text)
        teach.append(temp_review)

    for review in teach:
        print(review.grade)
    """
    # grab the next page 
    pages = class_page.find('div', 'paginator')
    span = pages.find_all('a')
    if span[1].text == 'disabled':
        print('zero')
        return 0
    else:
        print('directing to', span[1].get('href'), '\n')

        return span[1].get('href')


    






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

egg = Professor('Eggert')

#grab_classes("/professors/paul-r-eggert/com-sci-35l/", egg)
through_class("/professors/paul-r-eggert/com-sci-35l/")




