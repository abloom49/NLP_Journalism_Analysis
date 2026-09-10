from bs4 import BeautifulSoup
import requests
import pandas as pd

html_text = requests.get('https://www.babymed.com/baby-names/most-popular-1000-baby-names-1980s').text
soup = BeautifulSoup(html_text, 'lxml')


# total_jobs = soup.find_all('p')
total_jobs = soup.find('div', class_ = "field-item even")

mylist = []
for job in total_jobs:
    for item in job:
        # print(item, item.text, "BOTH")
        if type(item) != str:
            if len(item.text) > 0:
                if item.text[0] != "<" and item.text[0].isnumeric():
                    # print( item.text)
                    mylist.append(item.text)
numbers = []
girls = []
boys = []
for item in mylist:
    items = item.split()
    numbers.append(items[0])
    boys.append(items[1].lower())
    girls.append(items[4].lower())




df = pd.DataFrame({'numbers': numbers, 'boys': boys, 'girls': girls})
df.to_csv('names.csv', index = False, encoding = 'utf-8')

# job = soup.find('div', class_='dateblock')
# print(job)

# print(job.find('span', class_ = 'date').text.replace(' ',''))
# company_name = job.find('p').text.replace(' ','')
# skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')






#
# def genderfinder(name):
#     names = open('namespractice', 'r')
#     number = boys[name] - girls[name]
#     if number >0:
#         return "m"
#     else:
#         return "f"