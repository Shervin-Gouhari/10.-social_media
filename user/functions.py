from datetime import datetime


def YEARS():
    years = []
    year = datetime.now().year - 99
    for i in range(100):
        years.append(year)
        year += 1
    return years
