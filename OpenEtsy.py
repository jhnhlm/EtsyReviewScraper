from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
import time


#Ask user which Etsy store they want to scrape. 
etsy = input('What is the shop name? ')
driver = webdriver.Chrome('chromedriver')
driver.get("https://www.etsy.com/shop/{}".format(etsy))

#code to get review and put it into a dataframe
def get_review():
    reviews = driver.find_elements_by_xpath('//*[@id="reviews"]/div/div/div/ul/li/div/div/div')
    review_list = []
    for review in reviews:
        z = review.text
        review_list.append(z.split('\n'))
    x = pd.DataFrame(review_list)
    x.columns = ['name_date', 'rating', 'review', 'item']
    x.dropna(axis=0, inplace=True)
    return x

#get the length of reviews in an Etsy store
def max_page():
    maximum_pages = driver.find_elements_by_xpath('//*[@id="reviews"]/div/div/div[2]/div[4]/nav/ul')
    numbers = []
    pages = []
    for x in maximum_pages:
        pg = x.text
        pages.append(pg.split('\n'))
    for i in pages[0]:
        if i.isdigit():
            numbers.append(int(i))
    return max(numbers)

#clicking next
def click_next():
    element = driver.find_element_by_partial_link_text('Next page')
    element.click()
    driver.implicitly_wait(5)

pg_length = max_page()

review_table = []


for i in range(1, pg_length):
    m = get_review()
    m["page"] = i
    review_table.append(m)
    click_next()
    time.sleep(1)