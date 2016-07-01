#!/usr/bin/python
import sys
import numpy as np
import csv
import psycopg2
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

action = [
        "Rebound",
        "Free Throw",
        "Foul",
        "shot",
        "Turnover",
        "Tip Shot",
        "3pt Shot",
        "Jump Shot",
        "Layup",
        "Driving Layup",
        "Substitution",
        "Putback",
        "Dunk",
        "Timeout",
        "gains Possession",
        "Violation"
    ]
secondAction = [
        "Steal",
        "Assist"
        ]

class GameData:
    data = []
    def __init__(self, GameID, data):
        self.GameID = GameID
        self.data = data
    def append(self, data):
        self.data.append(data)

class userGameData:
    data = []
    def __init__(self, GameID, playerID):
        self.GameID = GameID
        self.playerID = playerID
    def append(self, data):
        self.data.append(data)
    def __str__(self):
        ret = ""
        for event in self.data:
            ret += str(event[0]) + " " + event[1] + "\n"
        return ret

def createPlaysTable(cur):
    execString = "CREATE TABLE plays (  game_id varchar(50) NOT NULL, play_no int NOT NULL, time_left varchar(50) NOT NULL, team varchar(3) NOT NULL, first_player varchar(50) NOT NULL, first_action varchar(50) NULL, first_stat varchar(50) NULL, second_player varchar(50) NULL, second_action varchar(50) NULL, second_stat varchar(50) NULL )"
    print(execString)
    try:
        cur.execute(execString)
    except psycopg2.Error as e:
        print("Table could not be created")
        print e.pgerror
        pass

def insertIntoPlaysTable(cur, databaseLine):
    execString = "INSERT INTO plays VALUES ("
    for i, cell in enumerate(databaseLine):
        execString += """ %s """
        if i < len(databaseLine)-1:
            execString += ","
    execString += ")"
    try: 
        cur.execute(execString, (databaseLine[0], databaseLine[1], databaseLine[2], databaseLine[3], databaseLine[4], databaseLine[5], databaseLine[6], databaseLine[7], databaseLine[8], databaseLine[9]))
    except psycopg2.Error as e:
        print e.pgerror
        pass

def GetConfigString(section):
    dict1 = {}
    ret = ""
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
        ret = ret + option + "='" + dict1[option] +"' "
    print(ret)
    return ret

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def parseLine(line):
    score = player = stat = playerAction = secondPlayer = secondPlayerAction = secondStat = ""
    desc = line[3]
    team = desc[1:4]
    indexOfSq = desc.find(']')
    if desc[5] == " ":
        score = desc[5:indexOfSq]
    if desc.find('(') != -1:
        endBracket = desc.find(')')
        stat = desc[desc.find('(')+1:endBracket]
        if endBracket != len(desc) -1: # has secondary stuff
            for possibleSecondAction in secondAction:
                if desc.lower().find(possibleSecondAction.lower()) != -1:
                    firstSpace = desc.find(":", endBracket)+1
                    secondPlayerAction = possibleSecondAction
                    secondPlayer = desc[firstSpace:desc.find("(", firstSpace+1)-1]
                    secondStat = desc[desc.rfind("(")+1:desc.rfind(")")]
    if (stat == "") & (desc.lower().find("missed") != -1):
        stat = "Missed"
    for possibleAction in action:
        if desc.lower().find(possibleAction.lower()) != -1:
            player = desc[indexOfSq+2:desc.lower().find(possibleAction.lower())-1]
            playerAction = possibleAction
        if playerAction == "Substitution":
            secondPlayer = desc[desc.find("by")+3:]

    return [line[0], line[1], line[2], team, player, playerAction, stat, secondPlayer, secondPlayerAction, secondStat]

if sys.argv[1] == "--help":
    print("parseNBAData.py [season]")
    print("season: season of txt file")
else: 
    textData = []
    parsedData = {}
    try:
        conn = psycopg2.connect(GetConfigString("database"))
        conn.autocommit = True
    except:
        print "I am unable to connect to the database"

    cur = conn.cursor()
    createPlaysTable(cur)

    with open('./'+ sys.argv[1] +'.txt', 'rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = "\t")
        currentGameId = ""
        for i, line in enumerate(tsvin):
            print("Inputing line "+str(i))
            if i > 1 & line[3].find("End of") != 0:
                databaseLine = parseLine(line)
                insertIntoPlaysTable(cur, databaseLine) 
        cur.close()




