from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
#set chromodriver.exe path
driver = webdriver.Chrome()
import time


def scrapePage(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    greetings = ["thank you", "thanks"]

    total_jobs = soup.find('div', class_ = "transcript storytext")
    jobs = total_jobs.find_all('p')
    nextline = False
    thankYou  = 0
    for job in jobs:
        if thankYou == 2:
            thankYou = 0
        stripped = job.text
        stripped = stripped.replace('(CHEERING)', "")
        stripped = stripped.replace('(SOUNDBITE OF MUSIC)', "")

        stripped = stripped.replace("Copyright © 2023 NPR.  All rights reserved.  Visit our website terms of use and permissions pages at www.npr.org for further information.", "")
        stripped = stripped.replace("NPR transcripts are created on a rush deadline by an NPR contractor. This text may not be in its final form and may be updated or revised in the future. Accuracy and availability may vary. The authoritative record of NPR’s programming is the audio record.", "")
        if stripped != "" and stripped[0:5] != "(SOUN":
            alreadyPrinted = False
            for word in greetings:
                if word in stripped.lower():
                    print(stripped)
                    thankYou += 1
                    alreadyPrinted = True
            if thankYou == 1 and alreadyPrinted == False:
                print(stripped)
                thankYou = 0


def main():


    #launch URL
    driver.get("https://www.npr.org/podcasts/510318/up-first")




    # Specify the common class name used for the buttons

    buttons = driver.find_elements(By.CLASS_NAME, "title")


    # Iterate through the list of buttons and click each one
    for i in range(len(buttons)):
        try:
            try:
                ourButton = driver.find_element(By.CLASS_NAME, "pn-modal__close")
                print('YAYYYYY')
                ourButton.click()
            except:
                pass
            buttons = driver.find_elements(By.CLASS_NAME, "title")
            buttons[i].click()
            time.sleep(3)
            print(driver.title)
            try:
                button = driver.find_element(By.CLASS_NAME, "icn-transcript")
                button.click()
                scrapePage(driver.current_url)
                driver.back()
            except:
                print("No Transcript")

            driver.back()
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    # Close the WebDriver
    driver.quit()


main()