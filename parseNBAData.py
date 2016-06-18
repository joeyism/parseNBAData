#!/usr/bin/python
import numpy as np
import csv

class GameData:
    data = []
    def __init__(self, GameID, data):
        self.GameID = GameID
        self.data = data
    def append(self, data):
        self.data.append(data)

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

textData = []
parsedData = {}
with open('./small.tsv', 'rb') as tsvin:
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

        
print (parsedData[parsedData.keys()[0]].data)
        
