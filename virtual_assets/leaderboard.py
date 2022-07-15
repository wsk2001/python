from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("D:\\tools\\chromedriver\\chromedriver")

driver.get("https://btctools.io/stats/leaderboard")
driver.implicitly_wait(10)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
str0 = soup.prettify()
print(str0.strip())

# list = soup.select_one(' tbody')
# print(list)


driver.close()
driver.quit()
