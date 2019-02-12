import os
from datetime import datetime
import demjson
import json

class LinestarPageData:
    def __init__(self, url, date):
        self.url = url
        self.date = date
        self.compeitions = []

    def addCompetition(self, comp):
        self.compeitions.append(comp)

class LinestarPlayerObject:
    def __init__(self, id, name, owned, pos, team, sal):
        self.id = id
        self.name = name
        self.owned = owned
        self.pos = pos
        self.team = team
        self.sal = sal

class LinestarCompeition:
    def __init__(self, name, id, games):
        self.name = name
        self.id = id
        self.games = games
        self.gpp = False
        self.doubleUp = False
        self.players = []

    def isDoubleUpOrGPP(self):
        if "double" in self.name:
            self.doubleUp = True
        else:
            self.gpp = True

    def addPlayers(self, player):
        self.players.append(player)

    def getID(self):
        return self.id

class DateError(Exception):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
    def datePrint(self):
        print("Could not get data for this day: " + self.year + "-" + self.month + "-" + self.day)

def removeWhitespace(string):
    string = string.strip()
    string = string.replace('\n', '')
    string = string.replace('\r', '')
    string = string.replace(';', '')
    string = string.strip()

    return string

'''
* Function to form the get the compeition object
'''
def getAndFormCompetitions(soup):
    try:
        scripts = soup.find_all("script")[20]
        AllJSONText = scripts.text
        junk, slateJSONTextRight = AllJSONText.split("var slates =")
        slateJSONText, junk = slateJSONTextRight.split("var posMap = {")

        slateJSONText = removeWhitespace(slateJSONText)

        slateJSON = demjson.decode(slateJSONText)
        numberOfGames = slateJSON[0]['games']

        competitions = []
        competitionsHTML = soup.find(attrs={"id": "cbContestResult"}).find_all("option")
        for comp in competitionsHTML:
            compTitle = comp.text

            l1 = LinestarCompeition(compTitle.lower(), int(comp['value']), int(numberOfGames))
            l1.isDoubleUpOrGPP()
            competitions.append(l1)

        return competitions
    except Exception as e:
        return []

'''
* Function to retrieve the date from Linestar
'''
def dateFromLineStar(soup):
    dateHTML = soup.find('span', {'class': 'periodSelectionPeriodName'})
    dateText = dateHTML.text.strip()

    datetime_object = datetime.strptime(dateText, "%b %d, %Y")

    return datetime_object

'''
* Function to find the json of players and their projected ownership from Linestar
'''
def playerJSONRetrival(soup):
    scripts = soup.find_all("script")[20]
    AllJSONText = scripts.text
    junk, playerJSONTextRight = AllJSONText.split("var actualResultsDict =")
    playerJSONText, junk = playerJSONTextRight.split("function posMatch")

    playerJSONText = removeWhitespace(playerJSONText)

    playerJSON = demjson.decode(playerJSONText)

    return playerJSON


'''
* Function to find the json of players and their projected ownership from Linestar
'''
def playerRetrival(players, competition):
    idForComp = competition.getID()
    playersForComp = players[str(idForComp)]

    for player in playersForComp:
        p1 = LinestarPlayerObject(int(player['id']), player['name'], player['owned'],
                                  player['pos'], player['team'], player['sal'])
        competition.addPlayers(p1)

    return competition

def mapDateToLinestarID(day, month, year):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "date_ids.json")

    with open(path, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    myfile.close()

    linestarDateIDs = json.loads(data)
    dateKey = str(year) + "-" + str(month) + "-" + str(day)
    return linestarDateIDs[dateKey]