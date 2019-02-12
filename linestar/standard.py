from linestar import helpers
from bs4 import BeautifulSoup
import requests

def fanduel_nba_own_date(date):
    dateID = helpers.mapDateToLinestarID(date.day, date.month, date.year)
    url = "https://www.linestarapp.com/Ownership/Sport/NBA/Site/FanDuel/PID/" + str(dateID)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    competitions = helpers.getAndFormCompetitions(soup)
    currentDate = helpers.dateFromLineStar(soup)
    stringDate = str(currentDate.day) + "-" + str(currentDate.month) + "-" + str(currentDate.year)

    lPageData = helpers.LinestarPageData(url, stringDate)

    if len(competitions) >= 1:
        playerJSON = helpers.playerJSONRetrival(soup)
        for comp in competitions:
            upComp = helpers.playerRetrival(playerJSON, comp)
            lPageData.addCompetition(upComp)
        return lPageData
    else:
        raise helpers.DateError(date.day, date.month, date.year)

def fanduel_nba_own_date_range(date1, date2):
    competitionsMap = {}

    dateIDStart = helpers.mapDateToLinestarID(date1.year, date1.month, date1.day)
    dateIDEnd = helpers.mapDateToLinestarID(date2.year, date2.month, date2.day)

    badDates = []

    for x in range(dateIDStart, dateIDEnd):
        url = "https://www.linestarapp.com/Ownership/Sport/NBA/Site/FanDuel/PID/" + str(x)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        competitions = helpers.getAndFormCompetitions(soup)
        currentDate = helpers.dateFromLineStar(soup)
        stringDate = str(currentDate.year) + "-" + str(currentDate.month) + "-" + str(currentDate.day)

        lPageData = helpers.LinestarPageData(url, stringDate)

        if len(competitions) >= 1:
            playerJSON = helpers.playerJSONRetrival(soup)
            for comp in competitions:
                upComp = helpers.playerRetrival(playerJSON, comp)
                lPageData.addCompetition(upComp)

            competitionsMap[stringDate] = lPageData
        else:
            badDates.append(stringDate)
            competitionsMap[stringDate] = []

    if len(badDates) >= 1:
        print("Unable to get ownership data for following dates:")
        for date in badDates:
            print(date)

    return competitionsMap
