
# problem: too many scotts

# it would be best to have the file as |  name: y/n

# assuming that it doesn't take the host ones
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
    print(names_all)
    print(info_all)
    if len(names_all) != len(info_all):
        print("ERROR, LISTS ARE DIFFERENT LENGTHS")
    else:
        dict = {}
        for i in range(len(names_all)):
            if i>0:
                if names_all[i] in info_all[i-1]:
                    if names_all[i] not in dict:
                        dict[names_all[i]] = info_all[i]
    return dict





practice_data = ["SIMON: Authorities there say that more than 800 people have been killed. They expect that number to rise. Hundreds of more people are wounded as rescuers scramble to try to save them from the rubble. NPR's Ruth Sherlock joins us from Rome. Ruth, thanks so much for being with us.",
                        "RUTH SHERLOCK, BYLINE: Thank you, Scott.",
                        "SIMON: NPR's Ruth Sherlock on duty for us in Rome. Ruth, thanks so much for being with us.",
                        "SHERLOCK: Thanks so much, Scott.",
                        "SIMON: Lee Strubinger from South Dakota Public Broadcasting was at the event and joins us now. Lee, thanks so much for being with us.",
                        "LEE STRUBINGER, BYLINE: Yeah. You bet, Scott.",
                        "SIMON: Lee Strubinger from South Dakota Public Broadcasting. Thanks so much for being with us.",
                        "STRUBINGER: Yeah. You bet.",
                        "RASCOE: That's Gabriel Spitzer of NPR's Science Desk. Thank you so much, Gabriel.",
                        "SPITZER: You're welcome.",
                        "SIMON: Evie Stone is our senior supervising editor. Sarah Lucy Oliver is our executive producer. Gerry Holmes is our deputy managing editor. Thanks to all those people who lend their talents as well to Weekend Edition.",
                        "RASCOE: Which you can hear on the radio. Turn it on every Saturday and Sunday morning. Find your NPR stations at stations.npr.org. We'd be so happy for you to listen."]

putting_into_file(practice_data)

def analysing_thanks(file):
    thanks = open('file', 'r')
    # need to remove the host
    # for line in thanks:
    #     gender =