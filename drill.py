import pymongo
import time
import random

from pymongo import MongoClient
cluster = MongoClient('mongodb+srv://DarraghHoyne:hg8WhQKx2dXSuWb@cluster0.tftue.mongodb.net/discordBot?retryWrites=true&w=majority')
db = cluster['discordBot']
collection = db['Users']

while True:
    players = collection.find({'all':'all'})
    for player in players:
        mine = player['mine']
        stone = mine[0]
        coins = mine[1]
        sCap = mine[2]
        cCap = mine[3]
        lvl = mine[4]
        if stone < sCap:
            stone = int(stone)+lvl
        if coins < mine[3]:
            coins = int(coins)+lvl*random.randint(4,5)

        mine = [stone, coins, sCap, cCap, lvl]
        collection.update_one({'_id':player['_id']}, {'$set':{'mine':mine}})
        time.sleep(100)