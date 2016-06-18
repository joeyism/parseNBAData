#!/usr/bin/python
import sys
import numpy as np
import csv

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

if sys.argv[1] == "--help":
    print("parseNBAData.py [season] [gameID] [player]")
    print("season: season of txt file")
else: 
    userInputGameId = sys.argv[2]
    player = sys.argv[3]
    textData = []
    parsedData = {}
    thisUserGameData = userGameData(userInputGameId, player)
    with open('./'+ sys.argv[1] +'.txt', 'rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter = "\t")
        currentGameId = ""
        for i, line in enumerate(tsvin):
            if i > 0:
                timeInSeconds = 48 * 60 - get_sec(line[2])
                dataLine = line[2:4]
                dataLine[0] = timeInSeconds
                if currentGameId == "":
                    currentGameId = line[0]
                    parsedData[currentGameId] = GameData(currentGameId, [dataLine])
                elif currentGameId == line[0]:
                    parsedData[currentGameId].append(dataLine)
                    textData.append(line)
                else:
                    currentGameId = line[0]
                    parsedData[currentGameId] = GameData(currentGameId, [dataLine])
                
                if player in dataLine[1]:
                    thisUserGameData.append(dataLine)
    print(thisUserGameData)
