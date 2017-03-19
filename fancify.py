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
def getLineCode(line):
    if line == 0:
        return "#  O-----o  #"
    if line == 1:
        return "#   O---o   #"
    if line == 2:
        return "#    O-o    #"
    if line == 3:
        return "#     O     #"
    if line == 4:
        return "#    o-O    #"
    if line == 5:
        return "#   o---O   #"
    if line == 6:
        return "#  o-----O  #"
    if line == 7:
        return "#  o-----O  #"
    if line == 8:
        return "#   o---O   #"
    if line == 9:
        return "#    o-O    #"
    if line == 10:
        return "#     O     #"
    if line == 11:
        return "#    O-o    #"
    if line == 12:
        return "#   O---o   #"
    if line == 13:
        return "#  O-----o  #"
    if line == 14:
        return "#  o-----O  #"
    if line == 15:
        return "#   o---O   #"
    if line == 16:
        return "#    o-O    #"
    if line == 17:
        return "#     O     #"
    if line == 18:
        return "#    O-o    #"
    if line == 19:
        return "#   O---o   #"
    if line == 20:
        return "#  O-----o  #"
    if line == 21:
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

    if (maxLine + 13 + 5) > 119:
        print("Reached over 120 chars per line ")

    '''Process Array'''
    for line in range(len(data)):
        add = getLineCode(line % 21)
        spaces = maxLine - len(data[line]) + 5
        data[line] = data[line][0:-1] + (spaces * " ") + add + "\n"

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

    if (maxLine + 13 + 5) > 119:
        print("Reached over 120 chars per line ")

    '''Process Array'''
    for line in range(len(data)):
        data[line] = data[line][0:-19] + "\n"

    '''Write Lines back'''
    with open('Individual_fancyTest.py', 'w') as file:
        file.writelines(data)


unfancify()
