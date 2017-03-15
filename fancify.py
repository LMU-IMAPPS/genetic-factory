#  O-----o  #
#   O---o   #
#    O-o    #
#     O     #
#    o-O    #
#   o---O   #
#  o-----O  #
#  O-----0  #
#   O---o   #
#    O-o    #
#     O     #
#    o-O    #
#   o---O   #
#  o-----O  #
#  O-----o  #
#   O---o   #
#    O-o    #
#     O     #
#    o-O    #
#   o---O   #
#  o-----O  #


# Generator
def getLineCode(l):
    if l == 0:
        return "#  O-----o  #"
    if l == 1:
        return "#   O---o   #"
    if l == 2:
        return "#    O-o    #"
    if l == 3:
        return "#     O     #"
    if l == 4:
        return "#    o-O    #"
    if l == 5:
        return "#   o---O   #"
    if l == 6:
        return "#  o-----O  #"
    if l == 7:
        return "#  o-----O  #"
    if l == 8:
        return "#   o---O   #"
    if l == 9:
        return "#    o-O    #"
    if l == 10:
        return "#     O     #"
    if l == 11:
        return "#    O-o    #"
    if l == 12:
        return "#   O---o   #"
    if l == 13:
        return "#  O-----o  #"
    if l == 14:
        return "#  o-----O  #"
    if l == 15:
        return "#   o---O   #"
    if l == 16:
        return "#    o-O    #"
    if l == 17:
        return "#     O     #"
    if l == 18:
        return "#    O-o    #"
    if l == 19:
        return "#   O---o   #"
    if l == 20:
        return "#  O-----o  #"
    if l == 21:
        return "#  o-----O  #"


def fancify():
    ''' Calc Max Lenght of '''
    maxLine = 0
    with open('Individual_fancyTest.py', 'r') as file:
        for line in file:
            if len(line) > maxLine:
                maxLine = len(line)

    '''Read Data from file'''
    with open('Individual_fancyTest.py', 'r') as file:
        data = file.readlines()

    if (maxLine+13+5) > 119:
        print("Reached over 120 chars per line ")

    '''Process Array'''
    for line in range(len(data)):
        add = getLineCode(line % 21)
        spaces = maxLine - len(data[line]) + 5
        data[line] = data[line][0:-1] + (spaces*" ") + add + "\n"

    '''Write Lines back'''
    with open('Individual_fancyTest.py', 'w') as file:
        file.writelines(data)


def unfancify():
    ''' Calc Max Lenght of '''
    maxLine = 0
    with open('Individual_fancyTest.py', 'r') as file:
        for line in file:
            if len(line) > maxLine:
                maxLine = len(line)

    '''Read Data from file'''
    with open('Individual_fancyTest.py', 'r') as file:
        data = file.readlines()

    if (maxLine+13+5) > 119:
        print("Reached over 120 chars per line ")

    '''Process Array'''
    for line in range(len(data)):
        add = getLineCode(line % 21)
        spaces = maxLine - len(data[line]) + 5
        data[line] = data[line][0:-19] + "\n"

    '''Write Lines back'''
    with open('Individual_fancyTest.py', 'w') as file:
        file.writelines(data)


unfancify()