import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from dateutil.relativedelta import relativedelta
import datetime
import time
import random

driver = None

def crawlNewsContent(pre_url):
    for i in range(1, 4000, 10):
        link_list = []
        query_url = pre_url + str(i)
        driver.implicitly_wait(5)

        driver.get(query_url)

        # Naver news links xpath
        naver_xpath_one = "//ul[@class='type01']/li/dl/dd/a"
        naver_xpath_two = "//ul[@class='type01']/li/dl/dd//ul/li/span/a"

        # Collect Naver news links from each news section
        news_blocks_one = driver.find_elements_by_xpath(naver_xpath_one)
        news_blocks_two = driver.find_elements_by_xpath(naver_xpath_two)

        news_blocks = news_blocks_one + news_blocks_two

        for doc in news_blocks:
            link_list.append(doc.get_attribute("href"))

        # Get news data for each naver news link
        for element in link_list:
            news_content = {}
            driver.get(element)
            driver.implicitly_wait(1)

            content_xpath = "//div[@id='articleBodyContents']"
            news_content["news"] = driver.find_element_by_xpath(content_xpath).text

            print(json.dumps(news_content, ensure_ascii=False, default=default))

            time.sleep(random.randint(1, 3))
            driver.back()
            time.sleep(random.randint(1, 3))

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

# Adjust the url string to search 10 years of news for the particular keyword
def adjustDate():
    today_date = datetime.datetime.now()
    today = today_date.strftime("%Y-%m-%d")
    today = today.replace("-", ".")
    ten_years = today_date - relativedelta(years=10)
    ten_years_back = ten_years.strftime("%Y-%m-%d")
    ten_years_back = ten_years_back.replace("-", ".")

    today_straight = today.replace(".", "")
    ten_year_back_straight = ten_years_back.replace(".", "")

    return today, ten_years_back, today_straight, ten_year_back_straight

# Get the keyword to search and create basic url string
def createURL():
    URL = "https://search.naver.com/search.naver?&where=news&query="
    keyword = '반도체'
    # keyword = input("검색어를 입력해주세요: ")
    # keyword = keyword.join('""')
    query_url = URL + keyword
    print(query_url)
    pre_url = query_url + "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds="

    today, ten_year_back, today_straight, ten_year_back_straight = adjustDate()

    pre_url += ten_year_back + '&de=' + today + '&docid=&nso=so:r,p:from' + ten_year_back_straight + 'to' + today_straight + ',a:all&mynews=0&start='
    print(datetime.datetime.now().time())
    crawlNewsContent(pre_url)
    print(datetime.datetime.now().time())

# Initialize chrome driver
def initDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    global driver
    if not driver:
        driver = webdriver.Chrome("/Users/onursahil/PycharmProjects/keyword_timerange_crawling/chromedriver", chrome_options=options)
    createURL()

if __name__ == '__main__':
    initDriver()
