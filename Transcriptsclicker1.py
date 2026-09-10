# from bs4 import BeautifulSoup
# import requests
# from selenium import webdriver
# driver = webdriver.Chrome()
#
#
# driver.get('https://www.npr.org/podcasts/510318/up-first')
# link = driver.find_element_by_id('1197287438')
# link.click()
from selenium import webdriver
from selenium.webdriver.common.by import By
#set chromodriver.exe path
driver = webdriver.Chrome()

#launch URL
driver.get("https://www.tutorialspoint.com/index.htm")
#identify element
l =driver.finds_element(By.XPATH, "//*[@class='btn default check check green markAsChecked']")
#perform click
for i in l:
    i.click()
print("Page title is: ")
print(driver.title)
#close browser
driver.quit()