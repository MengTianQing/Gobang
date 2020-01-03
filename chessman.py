
list1 = [[100,80],[80,90],[60,40],[80,40]]

newlist = list(filter(lambda cm: cm[0] > cm[1] ,list1))

print(newlist)



def takeSecond(elem):
    return elem[1]

newlist.sort(key=takeSecond,reverse=True)

print(newlist)