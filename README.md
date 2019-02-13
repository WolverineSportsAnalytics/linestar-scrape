## Linestar Scrape

### Goals
**The goal of this project is to provide a person with a standardized format for getting linestar ownership data so that it can be used for better understanding daily fantasy competitions**

Example:
https://www.linestarapp.com/Ownership/Sport/NBA/Site/FanDuel/PID/420

In order to scrape this page, lots of tedious work would have to be done in order to pull data from this site that could only be used for a specific use case. Why not make a package that can be used by everyone? This page contains valueable information to fantasy players and can be used for many DFS data science applications.

### Installation
`pip install linestar-scrape`
* Be sure to update often to get the latest mapping from human datetime to linestar date id

### Methods
`fanduel_nba_own_date(date)`

Inputs:
* Python datetime

Output: Linestar Page Data Object containing Linestar Data For That Date

`fanduel_nba_own_date_range(date1, date2)`

Inputs:
* date1 = Python datetime for first date
* date2 = Python datetime for second date

Output: Linestar Map with Date String (YYYY-MM-DD) being the key and a Linestar Page Data Object being a value for inclusive range of dates

### Linestar Objects
**Linestar Page Data**

Object Name: LinestarPageData

Members
* date
* competitions (array of LinestarCompeition)
* url (link to url scraped)

**Linestar Competitions**

Object Name: LinestarCompeition

Members
* name (competition name)
* id (competition id)
* games (number of games for competition)
* gpp (True if GPP Competition)
* doubleUp (True if Double Up Competition)
* players (Array of LinestarPlayerObject)

**Linestar Players**

Object Name: LinestarPlayerObject

Members
* id (player id)
* name (player name)
* owned (percent owned, in float format (ie: 78.2))
* pos (position)
* team 
* sal (salary)


### Examples
`import linestar`

`single_data = linestar.standard.fanduel_nba_own_date(datetime(2019, 2, 10))`

`range_data = linestar.standard.fanduel_nba_own_date(datetime(2019, 2, 5), datetime(2019, 2, 10))`