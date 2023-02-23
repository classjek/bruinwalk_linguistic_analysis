import requests
from bs4 import BeautifulSoup
import time

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
        self.reviews = []

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
# maybe have this return a class object with the name of the class 
def through_class(class_name, href):

    # intialize Class object
    one_class = Class(class_name, href)

    # just put this in the for loop lol
    val = grab_classes(href, 'dummyName', one_class.reviews)

    # add reviews from each page to one_class's list of reviews
    # grab_classes will return 0 if there exist no more pages 
    while val != 0:
        val = grab_classes(val, 'dummyName', one_class.reviews)
    
    return one_class



# make this return 0 or the href of the next page 
# given an href for a page of reviews, this will grab the text and grade from each review and return a list of them 
def grab_classes(href, prof_name, revlist):

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


    # for each review, create a review object containing
    # the grade, title, and text of the review 
    for _ in reviews: 
        # create review object
        temp_review = Review(prof_name)
    
        # get grade attached to review 
        text = _.find('div', class_='grade-margin')
        temp_review.grade = get_grade(text.text)

        # get the text of the review, could be stored in multiple <p> components
        text = _.find('div', class_='expand-area review-paragraph')
        paragraph = text.find_all('p')
        # multi paragraph handling
        if len(paragraph) > 1:
            for p in paragraph: 
                temp_review.text = temp_review.text + ' ' + p.text
        else: 
            temp_review.text = paragraph[0].text

        #print(paragraph.text)
        revlist.append(temp_review)

    # grab the next page 
    pages = class_page.find('div', 'paginator')
    span = pages.find_all('a')
    if span[1].get('href') == None:
        return 0
    else:
        return span[1].get('href')

# need to add multi page for this
# give this an href to a professor and it will return a professor object
def all_classes(href):

    # load the professors page 
    prof_page = requests.get(web_add + href)
    try:
        prof_page.raise_for_status()
    except Exception as exc:
        print('There was a problem loading a professor\'s page: %s' % (exc))

    browse = BeautifulSoup(prof_page.text, 'html.parser')

    # get prof's name and initialize Professor object
    prof_obj = Professor(browse.find('div', class_='aggregate-header content-row').find('h2').text)

    # grab each of the professors classes as an element
    classes = browse.find_all('div', 'title-container')

    prof_classes = []

    for _ in classes:
        yohf = _.find('a').get('href')
        class_title = _.find('a').find('span').text
        prof_classes.append(yohf)
        print(class_title)
    prof_obj.classes = prof_classes
    return prof_obj


start_time = time.time()

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

# cycles throuhg each professor on the first page, callng all_classes and grabbing all of the classes that are prosent on their first page
"""
for _ in elems:
    profref = _.find('div', 'flex-container professor-meta-content').find('a').get('href')
    name = all_classes(profref)
    print(name.name, len(name.classes), '\n')

print('len elemens', len(elems))
"""


egg = Professor('Eggert')

#grab_classes("/professors/paul-r-eggert/com-sci-35l/", egg)
revlist = []

#test = through_class('COM SCI 35L', "/professors/paul-r-eggert/com-sci-35l/")
test = through_class('MGMT 289Y',"/professors/sebastian-edwards/mgmt-289y/")
print(len(test.reviews))
print('done')


end_time = time.time()
runtime = end_time - start_time

print(f"Runtimet: {runtime:.2f} seconds")





