#!/usr/bin/python
import sys
import numpy as np
import csv
import psycopg2

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
        "Substitution",
        "Putback",
        "Dunk",
        "Timeout"
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

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def parseLine(line):
    score = stat = playerAction = secondPlayer = secondPlayerAction = secondStat = ""
    desc = line[3]
    team = desc[1:4]
    indexOfSq = desc.find(']')
    if desc[5] == " ":
        score = desc[5:indexOfSq]
    player = desc[indexOfSq+2:desc.find(' ', indexOfSq+2)]
    if desc.find('(') != -1:
        endBracket = desc.find(')')
        stat = desc[desc.find('(')+1:endBracket]
        if endBracket != len(desc) -1: # has secondary stuff
            for possibleSecondAction in secondAction:
                if desc.lower().find(possibleSecondAction.lower()) != -1:
                    firstSpace = desc.find(":", endBracket)+1
                    secondPlayerAction = possibleSecondAction
                    secondPlayer = desc[firstSpace:desc.find(" ", firstSpace+1)]
                    secondStat = desc[desc.rfind("(")+1:desc.rfind(")")]
    if (stat == "") & (desc.lower().find("missed") != -1):
        stat = "Missed"
    for possibleAction in action:
        if desc.lower().find(possibleAction.lower()) != -1:
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
    with open('./'+ sys.argv[1] +'.txt', 'rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = "\t")
        currentGameId = ""
        for i, line in enumerate(tsvin):
            if i > 1 & line[3].find("End of") != 0:
                databaseLine = parseLine(line)
                print(line)
                print(databaseLine)




