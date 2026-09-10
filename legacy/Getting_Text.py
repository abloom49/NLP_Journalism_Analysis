from bs4 import BeautifulSoup
import requests

# Reference dataset of URLs used during testing. Retained here for legacy
# documentation and comparison with the local transcript-analysis workflow.
SAMPLE_TRANSCRIPT_URLS = [
    "https://www.npr.org/transcripts/g-s1-142496",
    "https://www.npr.org/transcripts/nx-s1-5962642",
    "https://www.npr.org/transcripts/nx-s1-5961340",
    "https://www.npr.org/transcripts/nx-s1-5947161",
    "http://npr.org/transcripts/nx-s1-5955787",
    "https://www.npr.org/transcripts/nx-s1-5948157",
    "https://www.npr.org/transcripts/nx-s1-5961152",
    "https://www.npr.org/transcripts/nx-s1-5937892-e1",
    "https://www.npr.org/transcripts/nx-s1-5955451",
]

html_text = requests.get('https://www.npr.org/transcripts/1198465242').text
# html_text = requests.get('https://www.npr.org/transcripts/521927719').text
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


# job = soup.find('div', class_='dateblock')
# print(job)

# print(job.find('span', class_ = 'date').text.replace(' ',''))
# company_name = job.find('p').text.replace(' ','')
# skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')


