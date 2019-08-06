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

        # NAVER NEWS LINKS XPATH
        naver_xpath_one = "//ul[@class='type01']/li/dl/dd/a"
        naver_xpath_two = "//ul[@class='type01']/li/dl/dd//ul/li/span/a"

        # COLLECT NEWS LINKS ON THE CURRENT PAGE
        news_blocks_one = driver.find_elements_by_xpath(naver_xpath_one)
        news_blocks_two = driver.find_elements_by_xpath(naver_xpath_two)

        news_blocks = news_blocks_one + news_blocks_two

        for doc in news_blocks:
            link_list.append(doc.get_attribute("href"))

        try:
            # THROW FOR LOOP FOR EACH NEWS LINK
            for element in link_list:
                news_content = {}
                driver.get(element)
                driver.implicitly_wait(1)

                # EXTRACT PUBLISH DATE
                publish_date = driver.find_element_by_xpath("//span[@class='t11']").text
                if '. 오후' in publish_date:
                    publish_date = publish_date.replace(". 오후", "")
                else:
                    publish_date = publish_date.replace(". 오전", "")

                news_content["published_date"] = datetime.datetime.strptime(publish_date, "%Y.%m.%d %I:%M")

                # EXTRACT NEWS CONTENT
                content_xpath = "//div[@id='articleBodyContents']"
                news_content["news"] = driver.find_element_by_xpath(content_xpath).text

                print(json.dumps(news_content, ensure_ascii=False, default=default))

                time.sleep(random.randint(1, 3))
                driver.back()
                time.sleep(random.randint(1, 3))
        except NoSuchElementException as e:
            last_date = publish_date
            print(last_date)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


# ADJUST THE TIME RANGE FOR 10 YEARS
def adjustDate():
    today_date = datetime.datetime.now()
    today = today_date.strftime("%Y-%m-%d")
    today = today.replace("-", ".")
    ten_years = today_date - relativedelta(months=3)
    ten_years_back = ten_years.strftime("%Y-%m-%d")
    ten_years_back = ten_years_back.replace("-", ".")

    today_straight = today.replace(".", "")
    ten_year_back_straight = ten_years_back.replace(".", "")

    return today, ten_years_back, today_straight, ten_year_back_straight


# GET THE KEYWORD TO SEARCH FOR
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


# INITIALIZE CHROMEDRIVER
def initDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    global driver
    if not driver:
        driver = webdriver.Chrome("/Users/onursahil/Documents/Developer/Naver-News-Keyword-Crawling/chromedriver", chrome_options=options)
    createURL()


if __name__ == '__main__':
    initDriver()
