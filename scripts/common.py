import sys

names = ['', 'first', 'second', 'third', 'fourth']


def badyear(yearName, position):
    raise Exception(
        'Invalid '+yearName+' - please provide a '+yearName+' in the range 1999 to 2050 as the '+names[position]+' argument')


def getYear(yearName, position):
    try:
        year = int(sys.argv[position])
    except:
        badyear(yearName, position)

    if year < 1999 or year > 2050:
        badyear(yearName, position)
    print(yearName+' : ' + str(year))
    return year


def getTaxYear():
    return getYear("Tax Year", 1)


def getBaseAndTaxYear():
    taxyear = getYear("Tax Year", 1)
    baseyear = getYear("Base Year", 2)
    return (taxyear, baseyear)
