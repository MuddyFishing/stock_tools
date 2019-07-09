import time,re
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"')
browser= webdriver.Chrome(chrome_options=options)
browser.get('http://www.mafengwo.cn/poi/5430915.html')
time.sleep(5)

browser.maximize_window()

data=browser.page_source
print(browser.page_source)
def source():
    wait = ui.WebDriverWait(browser, 1000)
    wait.until(lambda driver: browser.find_element_by_xpath('//a[@title="蜂蜂点评"]'))
    browser.find_element_by_xpath('//li[@data-scroll="commentlist"]/a[@title="蜂蜂点评"]').click()
    browser.get_screenshot_as_file(r'C:\Users\weidu\PycharmProjects\day21\pachong\test\点击点评.png')
    time.sleep(5)


    # browser.execute_script("window.scrollTo(0,100000)")
    # js = "var q=document.body.scrollTop=10000000"
    # js = "var q=document.body.scrollTop=1000000000"
    browser.execute_script("window.scrollTo(0,9000)")

    browser.get_screenshot_as_file(r'C:\Users\weidu\PycharmProjects\day21\pachong\test\滚动结束.png')
    # wait = ui.WebDriverWait(browser, 1000)
    # wait.until(lambda driver: browser.find_element_by_xpath('//a[@class="pi pg-next"]'))
    # print('good')
    # browser.find_element_by_xpath('//a[@class="pi pg-next"]').click()

    # browser.switch_to.frame(browser.find_element_by_xpath('//iframe'))

    browser.implicitly_wait(2)
    # browser.find_element_by_xpath('//a[@class="pi pg-next"]').click()
    # browser.find_element_by_class_name('.pi.pg-next').click()
    js3 = "var div = document.getElementsByClassName('pi pg-next'); div[0].click();"
    browser.execute_script(js3)

    time.sleep(10)
    browser.close()

# def parse():
#parse first request

#     pat = '<p class="rev-txt">[a-zA-Z]*(.*?)</p>'
#     comment_all= re.compile(pat).findall(data)
#     print(comment_all)
# #parse next request
#
#     a=next(source)
#     pat='<p class="rev-txt">[a-zA-Z]*(.*?)</p>'
#     comment=re.compile(pat).findall(a)
#     print(comment)
source()
