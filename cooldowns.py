from discord import client
import pymongo
import time
import discord

from pymongo import MongoClient
cluster = MongoClient('mongodb+srv://DarraghHoyne:hg8WhQKx2dXSuWb@cluster0.tftue.mongodb.net/discordBot?retryWrites=true&w=majority')
db = cluster['discordBot']
collection = db['Users']

client = discord.Client()

while True:
    players = collection.find({'all':'all'})
    for player in players:
        channel = client.get_channel(918909073569751113)
        if player['chopCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'chopCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'chopCD':-1}})
        if player['mineCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'mineCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'mineCD':-1}})
        if player['exploreCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'exploreCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'exploreCD':-1}})
        if player['huntCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'huntCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'huntCD':-1}})
        if player['advCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'advCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'advCD':-1}})
        if player['dailyCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'dailyCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'dailyCD':-1}})
        if player['battleCD']<=0:
            collection.update_one({'_id':player['_id']}, {'$set':{'battleCD':0}})
        else:
            collection.update_one({'_id':player['_id']}, {'$inc':{'battleCD':-1}})
    time.sleep(1)
    