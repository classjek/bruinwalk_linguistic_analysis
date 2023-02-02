from selenium import webdriver

url = 'https://www.bruinwalk.com/search/?category=professors'

driver = webdriver.Chrome()
driver.get(url)

print("It working")