import time

def dayFuture(dateNow, inc): # dateNow format : '19/7/2023'
    normalYear = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    leapYear = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    currentDict = {}
    isLeapYear = None
    date, month, year = dateNow.split("/")
    date, month, year = int(date), int(month), year

    if year.endswith("00"):
        if int(year)%400 == 0:
            isLeapYear = True
        else:
            isLeapYear = False
    else:
        if int(year)%4 == 0:
            isLeapYear = True
        else:
            isLeapYear = False

    if isLeapYear == True:
        currentDict = leapYear
    else:
        currentDict = normalYear

    year = int(year)
    maxDate = currentDict.get(month)
    maxMonth = 12
    result = date + inc
    while result > maxDate:
        month += 1
        result = result - maxDate
    while month > maxMonth:
        year += 1
        month = month - maxMonth

    while result < 1:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        maxDatePrev = currentDict.get(month)
        if result > 0:
            result = maxDatePrev - result
        else:
            result = maxDatePrev + result
    return str(result)+"/"+str(month)+"/"+str(year)

print(dayFuture("10/9/2023",40))