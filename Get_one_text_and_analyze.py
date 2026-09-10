from bs4 import BeautifulSoup
import requests
import pandas as pd

# Reference dataset of URLs used during testing. These are kept here so the
# older scripts retain the sample corpus information without changing the
# fetch-based workflow that still exists in this file.
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

# problem: need to not discard the first name, needed for the gender thing later on

def main():
    list = get_text()
    putting_into_file(list)


def get_text():
    html_text = requests.get('https://www.npr.org/transcripts/1198465242').text
    # html_text = requests.get('https://www.npr.org/transcripts/521927719').text
    soup = BeautifulSoup(html_text, 'lxml')

    greetings = ["thank you", "thanks"]

    total_jobs = soup.find('div', class_ = "transcript storytext")
    jobs = total_jobs.find_all('p')
    nextline = False
    thankYou  = 0
    return_list = []
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
                    return_list.append(stripped)
                    thankYou += 1
                    alreadyPrinted = True
            if thankYou == 1 and alreadyPrinted == False:
                print(stripped)
                return_list.append(stripped)
                thankYou = 0
    return return_list

def putting_into_file(data_list):
    names_all = []
    info_all = []
    # I have a list of all names
    for i in data_list:
        data = i.split(":")
        name = data[0]. replace(", BYLINE", "")
        name = name. lower()
        names = name.split()
        name = names[-1]
        quote = data[1].lower()
        quote = quote.strip()
        names_all.append(name)
        info_all.append(quote)
    if len(names_all) != len(info_all):
        print("ERROR, LISTS ARE DIFFERENT LENGTHS")
    else:
        dict = {}
        for i in range(len(names_all)):
            if i>0:
                if names_all[i] in info_all[i-1]:
                    if names_all[i] not in dict:
                        one_line = info_all[i-1]
                        words_said = one_line.split()
                        for word in range(len(words_said)):
                            words_said[word] = words_said[word].strip(".")
                        place = words_said.index(names_all[i])
                        first_name = words_said[place-1]
                        print(first_name, "FN")
# need to take the words from info_all
# then need to find what word the last name is
# then need to find the word before that and label it name
                        gender = genderfinder(first_name)
                        if "thank" in info_all[i]:
                            thanks_measure = 'y'
                        else:
                            thanks_measure = 'n'
                        dict[first_name] = [info_all[i], gender, thanks_measure]
    name = []
    responses = []
    gender = []
    thanks_measure = []
    for key in dict:
        name.append(key)
        print(key, dict[key])
        responses.append(dict[key][0])
        gender.append(dict[key][1])
        thanks_measure.append(dict[key][2])
    print(responses)
    df = pd.DataFrame({'names': dict.keys(), 'response': responses, 'gender':gender, 'if said thanks': thanks_measure})
    df.to_csv('responses.csv', index=False, encoding='utf-8')

    return dict

def genderfinder(name):
    names = open('names.csv', 'r')
    # each name contains a list for number of boys uses, number of girls
    name_dict={}
    next(names)
    for line in names:
        items = line.split(",")
        if not items[1] in name_dict:
            name_dict[items[1]] = [int(1000),int(1000)]
        girl = items[2].strip()
        if not girl in name_dict:
            name_dict[girl] = [int(1000),int(1000)]
    names = open('names.csv', 'r')
    next(names)
    # print(name_dict)
    for line in names:
        items = line.split(",")
        name_dict[items[1]][0] = (int(items[0]))
        girl = items[2].strip()
        name_dict[girl][1] = (int(items[0]))
    # print(name_dict)
    # print(name_dict[name][0], name_dict[name][1])
    if name in name_dict:
        number = name_dict[name][0] - name_dict[name][1]
    else:
        number = 0
    # print(number)
    if number < 0:
        return "m"
    if number > 0:
        return "f"
    else:
        return "unknown"

if __name__== "__main__":
    main()


# job = soup.find('div', class_='dateblock')
# print(job)

# print(job.find('span', class_ = 'date').text.replace(' ',''))
# company_name = job.find('p').text.replace(' ','')
# skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')


