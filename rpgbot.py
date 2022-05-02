import discord
import random
import logging
import pymongo
import math
import time

from pymongo import MongoClient
from discord.ext import commands

cluster = MongoClient('mongodb+srv://DarraghHoyne:hg8WhQKx2dXSuWb@cluster0.tftue.mongodb.net/discordBot?retryWrites=true&w=majority')
db = cluster['discordBot']
collection = db['Users']

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
author = ''
allHuntFinds = [[' :boar:boar', ' :wolf:wolf', ' :fox:fox', ' :bear:bear', ' :deer:deer', 'n :monkey_face:ape'],[' :lion_face:lion', ' :elephant:elephant', ' wildebeest', ' :zebra:zebra', ' cheetah'], 
                ['n arctic hare', ' :seal:seal', ' :penguin:penguin', 'n arctic fox', ' reindeer'], [' :bat:vampire bat', ' <:boa:928706110351896586>tree boa', ' <:centipede:928707572536578119>giant centipede', ' <:bigspider:928709395423060049>wandering spider'],
                [' jellyfish', ' :shark:shark', ' :octopus:octopus', ' electric eel'], [' black bear', ' wolverine', ' moose']]
alladvFinds = [[' <:jaguar:924307398070513694>jaguar', ' :ninja:ninja', ' <:tribesman:924307893438808104>tribesman', ' :snake:viper'], 
            [' <:sandmonster:926963456140263435>sand monster', ' :hippopotamus:hippo', ' :rhino:rhino', ' :snake:adder'], [ 'polar bear', 'n eskimo warrior', 'n ice king', ' blue dragon'],
            [' green anaconda', ' piranha', 'n alligator', ' <:jaguar:924307398070513694>jaguar'], [' megalodon', ' sea monster',  ' :squid:giant squid', ' :ghost:pirate\'s ghost'],
            [' idk']]
exploreFinds = [' found an abandoned shack in the woods and searched it.', ' found a magpie\'s nest in a tree.',
                ' found some stuff buried in a hole in the ground. Must have been someone\'s treasure hole.',
                ' found an old temple of sorts. Seems like it could fall down any second.']
exploreItems = ['Tape', 'Nails', 'Glue Bottle', 'Rope']
armorLevels = ['No Armor', '<:leatherarmor:920078124664893581>Leather Armor', '<:chainmailarmor:922554281532461076>Chainmail Armor', '<:ironarmor:922560808158912574>Iron Armor',
             '<:goldarmor:922552951413813278>Gold Armor', '<:diamondarmor:926943977171730442>Diamond Armor', '<:emeraldarmor:927983842445385829>Emerald Armor', '<:rubyarmor:931911398450163744>Ruby Armor',
             '<:icearmor:936018609732460625>Ice Armor']
swordLevels = ['No Sword', '<:woodensword:922573413313302648>Wooden Sword', '<:stonesword:921829368785956864>Stone Sword', '<:ironsword:922561172425805824>Iron Sword',
             '<:goldsword:922562989457027073>Gold Sword', '<:diamondsword:926941886437003324>Diamond Sword', '<:emeraldsword:927982823065919529>Emerald Sword', '<:rubysword:931911450988007476>Ruby Sword',
             '<:icesword:936017933723901962>Ice Sword']
areas = ['1: The Forest', '2: The Savannah', '3: The Tundra', '4: The Tropics', '5: The Ocean', '6: The Mountains']

fight_id = None
fighter = None

def timeConversion(seconds):
    if seconds > 3600:
        hours = math.floor(seconds/3600)
        seconds = seconds%3600
        if seconds > 60:
            minutes = math.floor(seconds/60)
            seconds = seconds%60
            time = '{}h {}m {}s'.format(str(hours), str(minutes), str(seconds))
        else:
            time = '{}h {}m {}s'.format(str(hours), '0', str(seconds))
    elif seconds > 60:
        minutes = math.floor(seconds/60)
        seconds = seconds%60
        time = '{}m {}s'.format(str(minutes), str(seconds))
    else:
        time = '{}s'.format(str(seconds))
    return time

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event

async def on_message(message):
    global armorLevels
    global swordLevels
    global allhuntFinds
    if message.author == bot.user:
        return
    author = str(message.author)
    msg = message.content.lower()
    channel = message.channel
    player = collection.find_one({'_id':author})
    if player == None:
        if msg.startswith('cr'):
            if msg == 'cr start':
                collection.insert_one({'_id':author, 'level':1, 'area':'1: The Forest', 'health':100, 'coins':0, 'xp':0, 'maxXP':2000, 'max health':100, 'attack':20, 'defence':20,
                                        'armorNum':0, 'swordNum':0, 'healPotions':5, 'logs':0, 'stone':0, 'Tape':0, 'Glue Bottle':0, 'Nails':0, 'Rope':0, 'armorPieces':0,
                                        'swordPieces':0, 'areaN':1, 'pieceRarity':10, 'coincap':2000, 'chest':'No Chest', 'chestCapacity':0, 'chestCoins':0, 'chopCD':0, 'mineCD':0,
                                        'huntCD':0, 'exploreCD':0, 'advCD':0, 'battleCD':0, 'dailyCD':0, 'all':'all', 'prefix':'cr ', 'mine':[0, 0, 0, 0, 0]})
                await channel.send('Welcome to Cool Rpg!\nTo begin, you can `cr hunt` and go on `cr adventure` to gain coins and xp. But make sure to `cr heal` so you don\'t die\n'+
                                            '<:leatherarmor:920078124664893581>Once you have enough coins, you can buy basic armor and sword from the shop. You will then start finding precious armor'+
                                            ' and sword pieces in hunt and adventure, which can be used along with your coins to upgrade your equipment.<:ironsword:922561172425805824>\n'+
                                            '<:tape:923299842170695730>You can gather logs from `cr chop` and other items from `cr explore`. When you have '+
                                            'enough items, you can craft a boat and sail to the next area:nut_and_bolt:\nGo mining to get stone, which can be used'+
                                            'with wood to make an automatic drill. This will mine stone and precious metals for you while you are away, and can be upgraded')
            else:
                await channel.send('Use `cr start` to begin your cool rpg journey!')
            return
    else:
        prefix = player['prefix']
        level = player['level']
        area = player['area']
        health = int(player['health'])
        maxHealth = player['max health']
        coins = player['coins']
        xp = player['xp']
        maxXP  = player['maxXP']
        attack = player['attack']
        defence = player['defence']
        armorNum = player['armorNum']
        swordNum = player['swordNum']
        healPotions = player['healPotions']
        logs = player['logs']
        stone = player['stone']
        tape = player['Tape']
        nails = player['Nails']
        glueBottle = player['Glue Bottle']
        rope = player['Rope']
        armorPieces = player['armorPieces']
        swordPieces = player['swordPieces']
        pieceRarity = player['pieceRarity']
        chest = player['chest']
        chestCapacity = player['chestCapacity']
        chestCoins = player['chestCoins']
        areaN = player['areaN']
        coincap = player['coincap']
        mine = player['mine']
        mStone = mine[0]
        mCoins = mine[1]
        mStoneCap = mine[2]
        mCoinCap = mine[3]
        mLvl = mine[4]


        if msg.startswith(prefix+'help'):
            if msg.lower().lstrip(prefix+'help  ') == '':
                embed = discord.Embed(title='**COOL RPG HELP**', description='**Commands with cooldown:** '+prefix+'help commands\n**All Items: **'+prefix+'help items'+
                                    '\n**Armor and Sword: **'+prefix+'help gear\n**Areas: **'+prefix+'help area\n**Coins and Chests: **'+prefix+'help coins')
                await channel.send(embed=embed)
            elif msg.startswith(prefix+'help command'):
                embed = discord.Embed(title='**Commands with cooldown**', description='**Hunt:** You will search around and find a random mob. If you defeat it you will gain coins and XP.\n'+
                                '**Chop:** You will chop down some trees and get 4-10 logs\n**Explore: **You look around and find some tape, glue, rope or nails.\n'+
                                '**Adventure: **You will go on an adventure and find a powerful enemy. If you defeat them you will get lots of coins and XP, but be careful, many have died while fighting these enemies.')
                await channel.send(embed=embed)
            elif msg.startswith(prefix+'help item'):
                embed = discord.Embed(title='**Items**', description='**Heal Potions: **These magical potions will restore your health.\n**Logs: **You can get these by chopping trees, '+
                                    'and either sell them for coins or use them for crafting (check '+prefix+'recipes).\n**Tape, Glue Bottles, Rope and Nails: **These items are all found while '+
                                    'exploring and are used to craft the boat. You can also buy them from the shop for a high price. If you have extra, you can also sell them, but it is better to keep them for the next area')
                await channel.send(embed=embed)
            elif msg.startswith(prefix+'help gear'):
                embed = discord.Embed(title='**Armor and Sword**', description='**<:leatherarmor:920078124664893581>Basic Armor and Sword<:woodensword:922573413313302648>:**'+
                                    ' These can be bought from the shop for 500 coins each and will add an additional 10 attack and defence\n'+
                                    '**<:chainmailarmor:922554281532461076>Upgraded Armor and Sword<:ironsword:922561172425805824>: ** '+
                                    'Once you have bought the basic armor and sword, you will randomly find armor and sword pieces in hunt and adventure (much more common in  adventure). '+
                                    'Once you gather 5 of them, they can be used to upgrade your tools along with 1000 coins. The pieces become rarer the more you upgrade your tools. Each level gives +20 attack and defence')
                await channel.send(embed=embed)
            elif msg.startswith(prefix+'help area'):
                embed = discord.Embed(title='**Areas**', description='**Moving through areas: **To go to the next area you have to craft a boat, using logs and the items'+
                                    ' you find while exploring.\n**Changes in areas: **When you move up areas the enemies will become stronger so you will lose more health. '+
                                    'But don\'t worry, you will be rewarded with more XP and coins. Your coincap will also increase in higher areas\n**New commands unlocked: **_Coming Soon_')
                await channel.send(embed=embed)
            elif msg.startswith(prefix+'help coin'):
                embed = discord.Embed(title='**<:coin:925460192907374632>Coins and Chests<:coin:925460192907374632>: **', description='**Coincap: **The coincap for area 1 is 2000 and it increases by 2000 every area.'+
                                    ' To hold more coins, craft a chest\n**Chests: **Chests are crafted with logs and you can deposit coins into them when you reach your coincap. '+
                                    'There are 4 types of chests: small, medium, large and mega (check '+prefix+'recipes)\n**Earning Coins: **You can earn coins in hunt and adventure, and also by selling logs.'+
                                    '\n**Uses for Coins: **You can buy stuff in the shop with your coins. Coins are also needed along with sword/armor pieces to upgrade your sword/armor.')
                await channel.send(embed=embed)
        
        if msg.startswith(prefix+'recipe'):
            embed = discord.Embed(title='**Recipes**', description='**Small Chest: **60:wood:\n**Medium Chest: **120:wood:\n**Large Chest: **220:wood:\n'+
                                '**Mega Chest: **500:wood:\n**Boat: **'+str(140+areaN*60)+':wood:, {}<:tape:923299842170695730>, {}:nut_and_bolt:, '.format(str(12+areaN*8), str(12+areaN*8))+
                                '{}<:glue:923298482436063313>, {}<:rope:923299926543327262>'.format(str(12+areaN*8), str(12+areaN*8))+'\n**Upgraded Armor/Sword: **'+
                                '5<:armorpiece:925459954926768169>/<:swordpiece:925458435250745375>, 1000<:coin:925460192907374632> (uses '+prefix+'upgrade)')
            await channel.send(embed=embed)

        if msg.startswith(prefix+'prefix'):
            if msg.endswith('_'):
                msg = msg[:-1]
                msg += ' '
            if msg == prefix+'prefix':
                embed = discord.Embed(description = 'Use `'+prefix+'prefix [new prefix]` to set your prefix. If you want a space after your prefix, put a `_` after it'+
                '\ne.g. `{}prefix c` will mean chunt will work. `{}prefix c_` will mean c hunt will work.\nIf you forget your prefix, cr prefix will always work')
                await channel.send(embed=embed)
                
            else:
                newprefix = msg[len(prefix)+7:]
                collection.update_one({'_id':author}, {'$set':{'prefix':newprefix}})
                await channel.send('Your prefix was succesfully changed to '+newprefix)

        if msg.startswith(prefix+'buy '):
            if msg.startswith(prefix+'buy heal potion'):
                numBought = msg.lstrip(prefix+'buy heal potions')
                if numBought == '':
                    numBought=1
                else:
                    numBought=int(numBought)
                if coins >= 50*numBought:
                    collection.update_one({'_id':author}, {'$inc':{'healPotions':numBought}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-(50*numBought)}})
                    await channel.send(str(numBought) + ' heal potions successfully bought for '+str(50*numBought)+' coins')
                else:
                    await channel.send('You don\'t have enough coins for this lol')
            elif msg.startswith(prefix+'buy wooden sword'):
                if swordNum == 0:
                    if coins >= 500:
                        collection.update_one({'_id':author}, {'$set':{'swordNum':1}})
                        collection.update_one({'_id':author}, {'$inc':{'attack':10}})
                        collection.update_one({'_id':author}, {'$inc':{'coins':-500}})
                        await channel.send('Wooden Sword succesfully bought for 500 coins')
                    else:
                        await channel.send('You don\'t have enough coins for this lol')
                else:
                    await channel.send('You have already bought this sword')
            elif msg.startswith(prefix+'buy leather armor'):
                if armorNum == 0:
                    if coins >= 500:
                        collection.update_one({'_id':author}, {'$set':{'armorNum':1}})
                        collection.update_one({'_id':author}, {'$inc':{'defence':10}})
                        collection.update_one({'_id':author}, {'$inc':{'coins':-500}})
                        await channel.send('Leather Armor succesfully bought for 500 coins')
                    else:
                        await channel.send('You don\'t have enough coins for this lol')
                else:
                    await channel.send('You have already bought this armor')

            elif msg.startswith(prefix+'buy tape'):
                numBought = msg.lstrip(prefix+'buy tape')
                if numBought == '':
                    numBought = 1
                elif numBought == 'all':
                    numBought = math.floor(coins/(300+areaN*400))
                else:
                    try:
                        numBought = int(numBought)
                    except TypeError:
                        await channel.send('Please provide a valid amount to buy')
                if coins >= (300+areaN*400)*numBought:
                    collection.update_one({'_id':author}, {'$inc':{'Tape':numBought}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-(300+areaN*400)*numBought}})
                    await channel.send(str(numBought)+' tape succesfully bought for {} coins'.format(numBought*(300+areaN*400)))
                else:
                    await channel.send('You don\'t have enough coins for this lol')
            
            elif msg.startswith(prefix+'buy rope'):
                numBought = msg.lstrip(prefix+'buy rope')
                if numBought == '':
                    numBought = 1
                elif numBought == 'all':
                    numBought = math.floor(coins/(300+areaN*400))
                else:
                    try:
                        numBought = int(numBought)
                    except TypeError:
                        await channel.send('Please provide a valid amount to buy')
                if coins >= (300+areaN*400)*numBought:
                    collection.update_one({'_id':author}, {'$inc':{'Rope':numBought}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-(300+areaN*400)*numBought}})
                    await channel.send(str(numBought)+' rope succesfully bought for {} coins'.format(numBought*(300+areaN*400)))
                else:
                    await channel.send('You don\'t have enough coins for this lol')
            
            elif msg.startswith(prefix+'buy glue') or msg.startswith(prefix+'buy glue bottle'):
                numBought = msg.lstrip(prefix+'buy glue bottle')
                if numBought == '':
                    numBought = 1
                elif numBought == 'all':
                    numBought = math.floor(coins/(300+areaN*400))
                else:
                    try:
                        numBought = int(numBought)
                    except TypeError:
                        await channel.send('Please provide a valid amount to buy')
                if coins >= (300+areaN*400)*numBought:
                    collection.update_one({'_id':author}, {'$inc':{'Glue Bottle':numBought}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-(300+areaN*400)*numBought}})
                    await channel.send(str(numBought)+' glue bottles succesfully bought for {} coins'.format(numBought*(300+areaN*400)))
                else:
                    await channel.send('You don\'t have enough coins for this lol')
            
            elif msg.startswith(prefix+'buy nail'):
                numBought = msg.lstrip(prefix+'buy nails')
                if numBought == '':
                    numBought = 1
                elif numBought == 'all':
                    numBought = math.floor(coins/(300+areaN*400))
                else:
                    try:
                        numBought = int(numBought)
                    except TypeError:
                        await channel.send('Please provide a valid amount to buy')
                if coins >= (300+areaN*400)*numBought:
                    collection.update_one({'_id':author}, {'$inc':{'Nails':numBought}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-(300+areaN*400)*numBought}})
                    await channel.send(str(numBought)+' nails succesfully bought for {} coins'.format(numBought*(300+areaN*400)))
                else:
                    await channel.send('You don\'t have enough coins for this lol')
        
        if msg.startswith(prefix+'sell'):
            if msg.startswith(prefix+'sell log'):
                numSold = msg.lstrip(prefix+'sell log')
                if numSold == '':
                    numSold = 1
                elif numSold == 'all':
                    numSold = logs
                else:
                    try:
                        numSold = int(numSold)
                    except TypeError:
                        await channel.send('Please provide a valid amount to sell')
                if logs-numSold <0:
                    await channel.send('You don\'t have that many of this item')
                collection.update_one({'_id':author}, {'$inc':{'logs':-numSold}})
                collection.update_one({'_id':author}, {'$inc':{'coins':10*numSold}})
                await channel.send(str(numSold)+' logs sold for '+str(10*numSold)+' coins')
            
            if msg.startswith(prefix+'sell tape'):
                numSold = msg.lstrip(prefix+'sell tapes')
                if numSold == '':
                    numSold = 1
                elif numSold == 'all':
                    numSold = tape
                else:
                    try:
                        numSold = int(numSold)
                    except TypeError:
                        await channel.send('Please provide a valid amount to sell')
                if tape-numSold <0:
                    await channel.send('You don\'t have that many of this item')
                collection.update_one({'_id':author}, {'$inc':{'Tape':-numSold}})
                collection.update_one({'_id':author}, {'$inc':{'coins':80*numSold}})
                await channel.send(str(numSold)+' tape sold for '+str(80*numSold)+' coins')

            if msg.startswith(prefix+'sell rope'):
                numSold = msg.lstrip(prefix+'sell ropes')
                if numSold == '':
                    numSold = 1
                elif numSold == 'all':
                    numSold = rope
                else:
                    try:
                        numSold = int(numSold)
                    except TypeError:
                        await channel.send('Please provide a valid amount to sell')
                if rope-numSold <0:
                    await channel.send('You don\'t have that many of this item')
                collection.update_one({'_id':author}, {'$inc':{'Rope':-numSold}})
                collection.update_one({'_id':author}, {'$inc':{'coins':80*numSold}})
                await channel.send(str(numSold)+' rope sold for '+str(80*numSold)+' coins')

            if msg.startswith(prefix+'sell glue bottle'):
                numSold = msg.lstrip(prefix+'sell glue bottles')
                if numSold == '':
                    numSold = 1
                elif numSold == 'all':
                    numSold = glueBottle
                else:
                    try:
                        numSold = int(numSold)
                    except TypeError:
                        await channel.send('Please provide a valid amount to sell')
                if nails-numSold <0:
                    await channel.send('You don\'t have that many of this item')
                collection.update_one({'_id':author}, {'$inc':{'Nails':-numSold}})
                collection.update_one({'_id':author}, {'$inc':{'coins':80*numSold}})
                await channel.send(str(numSold)+' nails sold for '+str(80*numSold)+' coins')
            
            if msg.startswith(prefix+'sell nail'):
                numSold = msg.lstrip(prefix+'sell nails')
                if numSold == '':
                    numSold = 1
                elif numSold == 'all':
                    numSold = nails
                else:
                    try:
                        numSold = int(numSold)
                    except TypeError:
                        await channel.send('Please provide a valid amount to sell')
                if glueBottle-numSold <0:
                    await channel.send('You don\'t have that many of this item')
                collection.update_one({'_id':author}, {'$inc':{'Glue Bottles':-numSold}})
                collection.update_one({'_id':author}, {'$inc':{'coins':80*numSold}})
                await channel.send(str(numSold)+' glue bottles sold for '+str(80*numSold)+' coins')
        
        if msg.startswith(prefix+'upgrade'):
            if msg == prefix+'upgrade armor' or msg == prefix+'upgrade a':
                if armorPieces >= 5 and coins >= 1000:
                    collection.update_one({'_id':author}, {'$inc':{'armorNum':1}})
                    collection.update_one({'_id':author}, {'$inc':{'defence':20}})
                    collection.update_one({'_id':author}, {'$inc':{'armorPieces':-5}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-1000}})
                    collection.update_one({'_id':author}, {'$inc':{'pieceRarity':5}})
                    await channel.send('Armor succesfully upgraded for 5 armor pieces and 1000 coins!\nYou now have '+armorLevels[armorNum+1])
                else:
                    await channel.send('You need 1000 coins and 5 armor pieces to do this')

            if msg == prefix+'upgrade sword' or msg == prefix+'upgrade s':
                if swordPieces >= 5 and coins >= 1000:
                    collection.update_one({'_id':author}, {'$inc':{'swordNum':1}})
                    collection.update_one({'_id':author}, {'$inc':{'attack':20}})
                    collection.update_one({'_id':author}, {'$inc':{'swordPieces':-5}})
                    collection.update_one({'_id':author}, {'$inc':{'coins':-1000}})
                    collection.update_one({'_id':author}, {'$inc':{'pieceRarity':5}})
                    await channel.send('Sword succesfully upgraded for 5 sword pieces and 1000 coins!\nYou now have '+swordLevels[swordNum+1])
                else:
                    await channel.send('You need 1000 coins and 5 sword pieces to do this')

        if msg.startswith(prefix+'craft'):
            if msg == prefix+'craft small chest':
                if chest == 'No Chest':
                    if logs >= 60:
                        collection.update_one({'_id':author}, {'$set':{'chest':'Small Chest'}})
                        collection.update_one({'_id':author}, {'$set':{'chestCapacity':5000}})
                        collection.update_one({'_id':author}, {'$inc':{'logs':-60}})
                        await channel.send('You crafted a small chest! Capacity:5000 <:coin:925460192907374632>')
                    else:
                        await channel.send('You need 60 logs to craft this. You have: '+str(logs)+'/60')
                else:
                    await channel.send('You already have a '+chest)

            if msg == prefix+'craft medium chest':
                if chest == 'No Chest' or chest == 'Small Chest':
                    if logs >= 120:
                        collection.update_one({'_id':author}, {'$set':{'chest':'Medium Chest'}})
                        collection.update_one({'_id':author}, {'$set':{'chestCapacity':10000}})
                        collection.update_one({'_id':author}, {'$inc':{'logs':-120}})
                        await channel.send('You crafted a medium chest! Capacity:10000 <:coin:925460192907374632>')
                    else:
                        await channel.send('You need 120 logs to craft this. You have: '+str(logs)+'/120')
                else:
                    await channel.send('You already have a '+chest)
            
            if msg == prefix+'craft large chest':
                if logs >= 220:
                    collection.update_one({'_id':author}, {'$set':{'chest':'Large Chest'}})
                    collection.update_one({'_id':author}, {'$set':{'chestCapacity':20000}})
                    collection.update_one({'_id':author}, {'$inc':{'logs':-220}})
                    await channel.send('You crafted a large chest! Capacity:20000 <:coin:925460192907374632>')
                else:
                    await channel.send('You need 220 logs to craft this. You have: '+str(logs)+'/220')
            
            if msg == prefix+'craft mega chest':
                if logs >= 500:
                    collection.update_one({'_id':author}, {'$set':{'chest':'Mega Chest'}})
                    collection.update_one({'_id':author}, {'$set':{'chestCapacity':45000}})
                    collection.update_one({'_id':author}, {'$inc':{'logs':-500}})
                    await channel.send('You crafted a large chest! Capacity:45000 <:coin:925460192907374632>')
                else:
                    await channel.send('You need 500 logs to craft this. You have: '+str(logs)+'/500')
                
            if msg == prefix+'craft boat':
                if logs >= 140+(areaN*60) and glueBottle >= 12+(areaN*8) and tape >= 12+(areaN*8) and rope >=12+(areaN*8) and nails>=12+(areaN*8): 
                    await channel.send('You constructed a boat and sailed to the next area. ')
                    collection.update_one({'_id':author}, {'$set':{'area':areas[areaN]}})
                    collection.update_one({'_id':author}, {'$inc':{'areaN':1}})
                    collection.update_one({'_id':author}, {'$inc':{'logs':-(140+areaN*60)}})
                    collection.update_one({'_id':author}, {'$inc':{'Glue Bottle':-(12+areaN*8)}})
                    collection.update_one({'_id':author}, {'$inc':{'Tape':-(12+areaN*8)}})
                    collection.update_one({'_id':author}, {'$inc':{'Rope':-(12+areaN*8)}})
                    collection.update_one({'_id':author}, {'$inc':{'Nails':-(12+areaN*8)}})
                    collection.update_one({'_id':author}, {'$inc':{'coincap':2000}})
                else:
                    if logs >= 140+(areaN*60): logsG = ':white_check_mark:'
                    else: logsG = ':x:'

                    if glueBottle >= 12+(areaN*8): glueG = ':white_check_mark:'
                    else: glueG = ':x:'

                    if tape >= 12+(areaN*8): tapeG = ':white_check_mark:'
                    else: tapeG = ':x:'

                    if rope >= 12+(areaN*8): ropeG = ':white_check_mark:'
                    else: ropeG = ':x:'

                    if nails >= 12+(areaN*8): nailG = ':white_check_mark:'
                    else: nailG = ':x:'
                    
                    await channel.send('You don\'t have enough items to craft this.\n'+logsG+' Logs: '+str(logs)+'/'+str(140+areaN*60)+'\n'+glueG+' Glue Bottles: '
                    +str(glueBottle)+'/'+str(12+areaN*8)+'\n'+tapeG+' Tape: '+str(tape)+'/'+str(12+areaN*8)+'\n'+ropeG+' Rope: '+str(rope)+'/'+str(12+areaN*8)
                    +'\n'+nailG+' Nails: '+str(nails)+'/'+str(12+areaN*8))
            
        if msg.startswith(prefix+'p') or msg.startswith(prefix+'profile'):
            if msg == prefix+'p' or msg == prefix+'profile':
                embed = discord.Embed(title=(str(message.author)[:-5]+'\'s Profile'), description='', colour=0x3498db)
                embed.set_author(name=message.author.display_name,  icon_url=message.author.avatar_url)
                embed.add_field(name='**Progress**', value='**Area: **'+area+'\n**Level:** '+str(level)+'\n**XP:** '+str(xp)+'/'+str(maxXP), inline=False)
                embed.add_field(name='**Stats**', value=':crossed_swords:**Attack:** '+str(attack)+'\n:shield:**Defence:** '+str(defence)+'\n:heart:**Health:** '+str(int(health))+'/'+str(maxHealth), inline=False)
                embed.add_field(name='**Equipment**', value=swordLevels[swordNum]+'\n'+armorLevels[armorNum], inline=True)
                embed.add_field(name='**Money**', value='<:coin:925460192907374632>**Coins:** '+str(coins)+'\n**'+chest+':** '+str(chestCoins)+'/'+str(chestCapacity), inline=True)
                await channel.send(embed=embed)
            
        
        if msg == prefix+'i' or msg == prefix+'inventory' or msg == prefix+'inv':
            inventory = (':wood:**Logs:** '+str(logs)+'\n:rock:**Stone: **'+str(stone)+'\n<:healpotion:922573312897466369>**Heal Potions:** '+str(healPotions)+'\n<:swordpiece:925458435250745375>**Sword Pieces: **'
                        +str(swordPieces)+'\n<:armorpiece:925459954926768169>**Armor Pieces: **'+str(armorPieces)+'\n<:tape:923299842170695730>**Tape:** '+str(tape)+'\n:nut_and_bolt:**Nails:** '+str(nails)+
                        '\n<:glue:923298482436063313>**Glue Bottles: **'+str(glueBottle)+'\n<:rope:923299926543327262>**Rope: **'+str(rope))
            embed = discord.Embed(title=(str(message.author)+'\'s Inventory'), description=inventory, colour=0x2ecc71)
            await channel.send(embed=embed)

        if msg == prefix+'drill':
            embed = discord.Embed(title=(str(message.author)[:-5]+'\'s Drill'), description='See your drill\'s stats here')
            embed.set_author(name=message.author.display_name,  icon_url=message.author.avatar_url)
            embed.add_field(name='**Stats**', value='**Level: **'+str(mLvl)+'\n**:rock:Stone/Hour: **'+str(mLvl*29)+'\n**<:coin:925460192907374632>Coins/Hour: **'+str(mLvl*134))
            embed.add_field(name='**Capacity**', value=':rock:**Stone: **'+str(mStone)+'\n**<:coin:925460192907374632>Coins: **'+str(mCoins)+'\n:rock:**Stone Capacity: **'+str(mStoneCap)+'\n**<:coin:925460192907374632>Coin Capacity: **'+str(mCoinCap)+'\nClaim these with `'+prefix+'drill claim`')
            embed.add_field(name='**Next Level**', value=':rock:**Stone: **'+str(40+mLvl*100)+'\n:wood:**Logs: **'+str(40+mLvl*20)+'\nUpgrade with `'+prefix+'drill upgrade`', inline=False)
            await channel.send(embed=embed)
        
        if msg == prefix+'drill upgrade':
            if logs >= 40+mLvl*20 and stone >= 40+mLvl*100:
                collection.update_one({'_id':author}, {'$inc':{'stone':-(40+mLvl*100)}})
                collection.update_one({'_id':author}, {'$inc':{'logs':-(40+mLvl*20)}})
                mLvl += 1
                mStoneCap += 40
                mCoinCap += 300
                mine = [mStone, mCoins, mStoneCap, mCoinCap, mLvl]
                collection.update_one({'_id':author}, {'$set':{'mine':mine}})
                await channel.send('Drill upgraded! Level '+str(mLvl-1)+' >> Level '+str(mLvl))
            else:
                if logs >= 40+(mLvl*20): logsG = ':white_check_mark:'
                else: logsG = ':x:'

                if stone >= 40+(mLvl*80): stoneG = ':white_check_mark:'
                else: stoneG = ':x:'

                await channel.send('You don\'t have enough items to upgrade your drill.\n'+logsG+' Logs: '+str(logs)+'/'+str(40+mLvl*20)+
                '\n'+stoneG+' Stone: '+str(stone)+'/'+str(40+mLvl*100))
        
        if msg == prefix+'drill claim':
            if mCoins >= 1 and mStone >= 1:
                collection.update_one({'_id':author}, {'$inc':{'stone':mStone}})
                collection.update_one({'_id':author}, {'$inc':{'coins':mCoins}})
                mine[0] = 0
                mine[1] = 0
                collection.update_one({'_id':author}, {'$set':{'mine':mine}})
                await channel.send('Your drill collected '+str(mStone)+':rock: and '+str(mCoins)+'<:coin:925460192907374632> while you were away')
            else:
                await channel.send('You drill hasn\'t mined yet')

        if msg == prefix+'shop':
            armorBought = ''
            armorBought1 = ''
            swordBought = ''
            swordBought1 = ''
            if armorNum != 0:
                armorBought = '~~**Bought**'
                armorBought1 = '~~'
            if swordNum != 0:
                swordBought = '~~**Bought**'
                swordBought1 = '~~'
            embed = discord.Embed(title='**RPG SHOP**', description='**Buy something with '+prefix+'buy [item]**\n\n<:healpotion:922573312897466369>**Heal Potion** cost: 50<:coin:925460192907374632>'+
                                    '\n'+armorBought1+'<:leatherarmor:920078124664893581>**Leather Armor** cost: 500<:coin:925460192907374632>'+armorBought+
                                    '\n'+swordBought1+'<:woodensword:922573413313302648>**Wooden Sword** cost: 500<:coin:925460192907374632>'+swordBought+
                                    '\n<:tape:923299842170695730>**Tape **cost: '+str(300+areaN*400)+'<:coin:925460192907374632>\n:nut_and_bolt:**Nail **cost: '+str(300+areaN*400)+'<:coin:925460192907374632>'+
                                    '\n<:glue:923298482436063313>**Glue Bottle **cost: '+str(300+areaN*400)+'<:coin:925460192907374632>\n<:rope:923299926543327262>**Rope **cost: '+str(300+areaN*400)+'<:coin:925460192907374632>')
            await channel.send(embed=embed)

        if msg == prefix+'heal':
            if healPotions > 0:
                collection.update_one({'_id':author}, {'$inc':{'healPotions':-1}})
                collection.update_one({'_id':author}, {'$set':{'health':maxHealth}})
                await channel.send('Your health has been restored')
            else:
                await channel.send('You need a <:healpotion:922573312897466369>heal potion to do this. Buy one in the shop')

        if msg.startswith(prefix+'dep') or msg.startswith(prefix+'deposit'):
            numDeposit = msg.lstrip(prefix+'deposit  ')
            try:
                int(numDeposit)
                isint = True
            except ValueError:
                if numDeposit == 'all':
                    numDeposit = coins
                    isint = True
                else: isint = False
            if numDeposit == '' or not isint:
                await channel.send('Please provide a valid amount to deposit')
            elif int(numDeposit)>coins or int(numDeposit)+chestCoins>chestCapacity:
                await channel.send('Please provide a valid amount to deposit')
            else:
                numDeposit = int(numDeposit)
                collection.update_one({'_id':author}, {'$inc':{'chestCoins':numDeposit}})
                collection.update_one({'_id':author}, {'$inc':{'coins':-numDeposit}})
                await channel.send(str(numDeposit)+' coins succesfully deposited')
        
        if msg.startswith(prefix+'withdraw'):
            numWithdraw = msg.lstrip(prefix+'withdraw  ')
            try:
                int(numWithdraw)
                isint = True
            except ValueError:
                if numWithdraw == 'all':
                    await channel.send('withdrawing all')
                    if coincap-coins > chestCoins:
                        numWithdraw = chestCoins
                    else: numWithdraw = coincap-coins
                    isint = True
                else: isint = False
            if numWithdraw == '' or not isint:
                await channel.send('Please provide a valid amount to withdraw')
            elif int(numWithdraw)>chestCoins: 
                await channel.send('You don\'t have this many coins in your chest')
            elif int(numWithdraw)+coins>coincap:
                await channel.send('You can\'t withdraw this many coins! It would exceed your coincap')
            else:
                numWithdraw = int(numWithdraw)
                collection.update_one({'_id':author}, {'$inc':{'coins':numWithdraw}})
                collection.update_one({'_id':author}, {'$inc':{'chestCoins':-numWithdraw}})
                await channel.send(str(numWithdraw)+' coins succesfully withdrawn')
        
        if msg == prefix+'rd' or msg == prefix+'ready':
            notRD = 0
            if player['huntCD'] == 0: 
                hready = ':white_check_mark: **Hunt: **Ready\n'
            else:
                hready = ''
                notRD+=1

            if player['chopCD'] == 0: 
                cready = ':white_check_mark: **Chop: **Ready\n'
            else:
                cready = ''
                notRD+=1

            if player['mineCD'] == 0: 
                mready = ':white_check_mark: **Mine: **Ready\n'
            else:
                mready = ''
                notRD+=1

            if player['exploreCD'] == 0: 
                eready = ':white_check_mark: **Explore: **Ready\n'
            else:
                eready = ''
                notRD+=1

            if player['advCD'] == 0: 
                aready = ':white_check_mark: **Adventure: **Ready\n'
            else:
                aready = ''
                notRD+=1

            if player['dailyCD'] == 0: 
                dready = ':white_check_mark: **Daily: **Ready\n'
            else:
                dready = ''
                notRD+=1
            
            if notRD == 6:
                hready = 'All commands on cooldown'
            
            embed = discord.Embed(title = author[:-5]+'\'s Ready', description = hready+cready+mready+eready+aready+dready)
            await channel.send(embed=embed)
        
        if msg == prefix+'cd' or msg == prefix+'cooldowns':
            if player['huntCD'] == 0: 
                hready = 'Ready'
                hready1 = ':white_check_mark:'
            else:
                hready = timeConversion(player['huntCD']*2)
                hready1 = ':clock1030:'

            if player['chopCD'] == 0: 
                cready = 'Ready'
                cready1 = ':white_check_mark:'
            else: 
                cready = timeConversion(player['chopCD']*2)
                cready1 = ':clock1030:'
            
            if player['mineCD'] == 0: 
                mready = 'Ready'
                mready1 = ':white_check_mark:'
            else: 
                mready = timeConversion(player['mineCD']*2)
                mready1 = ':clock1030:'

            if player['exploreCD'] == 0:
                eready = 'Ready'
                eready1 = ':white_check_mark:'
            else: 
                eready = timeConversion(player['exploreCD']*2)
                eready1 = ':clock1030:'

            if player['advCD'] == 0:
                aready = 'Ready'
                aready1 = ':white_check_mark:'
            else: 
                aready = timeConversion(player['advCD']*2)
                aready1 = ':clock1030:'
            
            if player['dailyCD'] == 0:
                dready = 'Ready'
                dready1 = ':white_check_mark:'
            else: 
                dready = timeConversion(player['dailyCD']*2)
                dready1 = ':clock1030:'
            
            embed = discord.Embed(title = author[:-5]+'\'s Cooldowns', description = hready1+' **Hunt:** '+hready+'\n'+cready1+' **Chop:** '+cready+'\n'
                    +mready1+' **Mine: **'+mready+'\n'+eready1+' **Explore:** '+eready+'\n'+aready1+' **Adventure: **'+aready+'\n'+dready1+' **Daily: **'+dready)
            await channel.send(embed=embed)

        if msg == prefix+'chop':
            if player['chopCD'] == 0:
                collection.update_one({'_id':author}, {'$set':{'chopCD':30}})
                logsGot = random.randint(4, 10)
                await channel.send(author[:len(author)-5]+' is chopping a tree. Got '+str(logsGot)+' logs')
                collection.update_one({'_id':author}, {'$inc':{'logs':logsGot}})
            else:
                await channel.send('**Still on cooldown** try again in {}'.format(timeConversion(player['chopCD']*2)))
        
        if msg == prefix+'mine':
            if player['mineCD'] == 0:
                collection.update_one({'_id':author}, {'$set':{'mineCD':150}})
                stoneGot = random.randint(2, 6)
                await channel.send(author[:len(author)-5]+' went mining. Got '+str(stoneGot)+' stone')
                collection.update_one({'_id':author}, {'$inc':{'stone':stoneGot}})
            else:
                await channel.send('**Still on cooldown** try again in {}'.format(timeConversion(player['mineCD']*2)))
                
        if msg == prefix+'hunt':
            if player['huntCD'] == 0:
                collection.update_one({'_id':author}, {'$set':{'huntCD':15}})
                coinsGot = random.randint(30+areaN*20, 80+areaN*20)
                xpGot = random.randint(110+areaN*40, 210+areaN*40)
                got_armor = random.randint(1, pieceRarity)
                got_sword = random.randint(1, pieceRarity)
                mobFound = random.choice(allHuntFinds[areaN-1])
                healthLost = math.floor(int(random.randint(areaN*7, 15+areaN*7)-(attack+defence)/20))
                if healthLost <= 0:
                    healthLost=random.randint(0,1)
                collection.update_one({'_id':author}, {'$inc':{'health':-healthLost}})
                health-=healthLost
                if health <=  0:
                    if level > 1:
                        collection.update_one({'_id':author}, {'$inc':{'level':-1}})
                        collection.update_one({'_id':author}, {'$inc':{'maxXP':-400}})
                        collection.update_one({'_id':author}, {'$set':{'xp':0}})
                        collection.update_one({'_id':author}, {'$inc':{'attack':-10}})
                        collection.update_one({'_id':author}, {'$inc':{'defence':-10}})
                        collection.update_one({'_id':author}, {'$set':{'health':maxHealth}})
                        await channel.send(author[:-5]+' found a'+mobFound+' but died fighting. You lost a level and all your XP')
                    else:
                        collection.update_one({'_id':author}, {'$set':{'xp':0}})
                        collection.update_one({'_id':author}, {'$set':{'health':maxHealth}})
                        await channel.send(author[:-5]+' found a'+mobFound+' but died fighting. You didn\'t lose a level because you are only level 1, but you lost all your XP')
                else:
                    await channel.send(author[:-5]+' found a' + mobFound + ' and killed it! \nLost '+ str(healthLost) +' health. Remaining health: '+str(int(health))+'/'+str(maxHealth)+'\nEarned ' + str(coinsGot) + ' coins and ' + str(xpGot) + 'XP')
                    collection.update_one({'_id':author}, {'$inc':{'coins':coinsGot}})
                    coins += coinsGot
                    collection.update_one({'_id':author}, {'$inc':{'xp':xpGot}})
                    if armorNum!=0 and armorPieces <5:
                        if got_armor == 5:
                            armorPieces += 1
                            collection.update_one({'_id':author}, {'$inc':{'armorPieces':1}})
                            if armorPieces <5:
                                await channel.send(author[:-5]+' got an armor piece! Collect 5 armor pieces to upgrade your armor. Current: '+str(armorPieces))
                            elif armorPieces == 5:
                                await channel.send(author[:-5]+' got an armor piece! You now have 5 armor pieces. Upgrade your armor with '+prefix+'upgrade armor')
                    if swordNum!=0 and swordPieces <5:
                        if got_sword == 5:
                            swordPieces += 1
                            collection.update_one({'_id':author}, {'$inc':{'swordPieces':1}})
                            if swordPieces <5:
                                await channel.send(author[:-5]+' got a sword piece! Collect 5 sword pieces to upgrade your sword. Current: '+str(swordPieces))
                            elif swordPieces == 5:
                                await channel.send(author[:-5]+' got a sword piece! You now have 5 sword pieces. Upgrade your sword with '+prefix+'upgrade sword')

                    if xp+xpGot >= maxXP:
                        newHealth = ''
                        collection.update_one({'_id':author}, {'$inc':{'level':1}})
                        collection.update_one({'_id':author}, {'$inc':{'xp':-maxXP}})
                        collection.update_one({'_id':author}, {'$inc':{'maxXP':400}})
                        collection.update_one({'_id':author}, {'$set':{'health':maxHealth}})
                        collection.update_one({'_id':author}, {'$inc':{'attack':10}})
                        collection.update_one({'_id':author}, {'$inc':{'defence':10}})
                        if (level+1)%10 == 0:
                            collection.update_one({'_id':author}, {'$inc':{'max health':50}})
                            newHealth = ' +50:heart:'
                        await channel.send(author[:-5]+' leveled up! You are now level '+str(level+1)+'. +10:crossed_swords:, +10:shield:'+newHealth+'. Your health has been restored')
            else:
                cd = timeConversion(player['huntCD']*2)
                await channel.send('**Still on cooldown**, try again in {}'.format(cd))
        
        if msg == prefix+'explore' or msg == prefix+'ex':
            if player['exploreCD'] == 0:
                collection.update_one({'_id':author}, {'$set':{'exploreCD':300}})
                numFound = random.randint(2, 4)
                typeFound = random.choice(exploreItems)
                await channel.send(author[:-5]+random.choice(exploreFinds)+' You got '+str(numFound)+' '+typeFound)
                collection.update_one({'_id':str(author)}, {'$inc':{typeFound:numFound}})
            else:
                await channel.send('**Still on cooldown**, try again in {}'.format(timeConversion(player['exploreCD']*2)))
        
        if msg.startswith(prefix+'adv'):
            if player['advCD'] == 0:
                collection.update_one({'_id':author}, {'$set':{'advCD':900}})
                coinsGot = random.randint(100+areaN*50, 300+areaN*50)
                xpGot = random.randint(200+areaN*100, 400+areaN*100)
                got_armor = random.randint(1, pieceRarity/5)
                got_sword = random.randint(1, pieceRarity/5)
                healthLost = math.floor(int(random.randint(15+areaN*11, 30+areaN*11)-(attack+defence)/20))          
                mobFound = random.choice(alladvFinds[areaN-1])
                if healthLost < 0:
                    healthLost=0
                collection.update_one({'_id':author}, {'$inc':{'health':-healthLost}})
                health-=healthLost
                if health <=  0:
                    if level > 1:
                        collection.update_one({'_id':author}, {'$inc':{'level':-1}})
                        collection.update_one({'_id':author}, {'$inc':{'maxXP':-400}})
                        collection.update_one({'_id':author}, {'$set':{'xp':0}})
                        collection.update_one({'_id':author}, {'$inc':{'attack':-10}})
                        collection.update_one({'_id':author}, {'$inc':{'defence':-10}})
                        collection.update_one({'_id':author}, {'$set':{'health':100}})
                        await channel.send(author[:-5]+' found a'+mobFound+' but died fighting. You lost a level and all your XP')
                    else:
                        collection.update_one({'_id':author}, {'$set':{'xp':0}})
                        collection.update_one({'_id':author}, {'$set':{'health':100}})
                        await channel.send(author[:-5]+' found a'+mobFound+' but died fighting. You didn\'t lose a level because you are only level 1, but you lost all your XP')
                else:
                    await channel.send(author[:-5]+' found a' + mobFound + ' and killed it! \nLost '+ str(healthLost) +' health. Remaining health: '+str(health)+'/'+str(maxHealth)+'\nEarned ' + str(coinsGot) + ' coins and ' + str(xpGot) + 'XP')
                    collection.update_one({'_id':author}, {'$inc':{'coins':coinsGot}})
                    coins += coinsGot
                    collection.update_one({'_id':author}, {'$inc':{'xp':xpGot}})
                    if armorNum!=0 and armorPieces <5:
                        if got_armor == 5:
                            armorPieces += 1
                            collection.update_one({'_id':author}, {'$inc':{'armorPieces':1}})
                            if armorPieces <5:
                                await channel.send(author[:-5]+' got an armor piece! Collect 5 armor pieces to upgrade your armor. Current: '+str(armorPieces))
                            elif armorPieces == 5:
                                await channel.send(author[:-5]+' got an armor piece! You now have 5 armor pieces. Upgrade your armor with '+prefix+'upgrade armor')
                    if swordNum!=0 and swordPieces <5:
                        if got_sword == 5:
                            swordPieces += 1
                            collection.update_one({'_id':author}, {'$inc':{'swordPieces':1}})
                            if swordPieces <5:
                                await channel.send(author[:-5]+' got a sword piece! Collect 5 sword pieces to upgrade your sword. Current: '+str(swordPieces))
                            elif swordPieces == 5:
                                await channel.send(author[:-5]+' got a sword piece! You now have 5 sword pieces. Upgrade your sword with '+prefix+'upgrade sword')

                    if xp+xpGot >= maxXP:
                        newHealth = ''
                        collection.update_one({'_id':author}, {'$inc':{'level':1}})
                        collection.update_one({'_id':author}, {'$inc':{'xp':-maxXP}})
                        collection.update_one({'_id':author}, {'$inc':{'maxXP':400}})
                        collection.update_one({'_id':author}, {'$set':{'health':100}})
                        collection.update_one({'_id':author}, {'$inc':{'attack':10}})
                        collection.update_one({'_id':author}, {'$inc':{'defence':10}})
                        if (level+1)%10 == 0:
                            collection.update_one({'_id':author}, {'$inc':{'max health':50}})
                            newHealth = ' +50:heart:'
                        await channel.send(author[:-5]+' leveled up! You are now level '+str(level+1)+'. +10:crossed_swords:, +10:shield:'+newHealth+'. Your health has been restored')
            else:
                await channel.send('**Still on cooldown**, try again in {}'.format(timeConversion(player['advCD']*2)))
            
        if msg == prefix+'daily':
            if player['dailyCD'] == 0:
                collection.update_one({'_id':author}, {'$inc':{'coins':300+level*60+random.randint(3, 25)}})
                collection.update_one({'_id':author}, {'$inc':{'healPotions':5+math.floor(level*0.7)}})
                collection.update_one({'_id':author}, {'$set':{'dailyCD':43200}})
                embed = discord.Embed(title=author[:-5]+'\'s Daily Reward', description='+{} coins<:coin:925460192907374632>\n+{} '.format(300+level*60+random.randint(3, 25), 5+level*1)+
                                    'heal potions<:healpotion:922573312897466369>')
                await channel.send(embed=embed)
            else:
                await channel.send('**Still on cooldown**, try again in {}'.format(timeConversion(player['dailyCD']*2)))
        if coins > coincap:
            collection.update_one({'_id':author}, {'$set':{'coins':coincap}})
            await channel.send(author[:-5]+' had too many coins so your coins have been set back to '+str(coincap))
        if msg.startswith('cr prefix '):
                if msg == 'cr prefix':
                    embed = discord.Embed(description = 'Use `cr prefix [new prefix]` to set your prefix. If you want a space after your prefix, put `_` after it'+
                    '\ne.g. `cr prefix c` will mean chunt will work. `cr prefix c_` will mean c hunt will work.\nIf you forget your prefix, cr prefix will always work')
                    await channel.send(embed=embed)
                else:
                    newprefix = msg[10:]
                    collection.update_one({'_id':author}, {'$set':{'prefix':newprefix}})
                    await channel.send('Your prefix was succesfully changed to '+newprefix+'\nYou can now use '+prefix+'hunt')
    await bot.process_commands(message=message)

bot.run('OTE5MzIxNDM5MzAyMTg5MDg2.YbUGzw.ZqkLFBA2Bj-AyBl9cht5a-8kwdQ')