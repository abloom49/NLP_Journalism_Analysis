
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
    number = name_dict[name][0] - name_dict[name][1]
    # print(number)
    if number < 0:
        return "m"
    if number > 0:
        return "f"
    else:
        return "unknown"

# positive is girl negative is boy
print(genderfinder("amelia"))
# genderfinder("Olivia")
# genderfinder("Claire")
# genderfinder("John")
# genderfinder('Adam')
# genderfinder('Alex')