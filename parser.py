#!/usr/bin/python3  

import urllib.request
import smtplib, ssl
import os, os.path
import json
from datetime import datetime

def main():
    config = loadConfig()
    if not config:
        exit(-1)
    if isOutOfStock(config['targetUrl']):
        Log.log(Log.info, 'item {0} is still out of stock'.format(config['targetUrl']))
    else:
        Log.log(Log.info, 'HURRAY! THE ITEM {0} IS NO LONGER OUT OF STOCK!'.format(config['targetUrl']))
        for receiver in config['receivers']:
            sendMail(config, receiver)

def isOutOfStock(url):
    # if this string is in the html body, the item is out of stock
    target = '<divclass="stock-container"><spanclass="stockstock--X"></span>Nichtverf'
    # fetch html from url and remove newline and whitespace
    html = urllib.request.urlopen(url).read()
    html = str(html).replace(' ', '').replace('\\n', '')
    return target in html

def loadConfig():
    # constants
    configPath = os.path.dirname(__file__)
    configFilename = os.path.join(configPath, 'config.json')
    defaultConfig = {'mailuser': '', 'password': '', 'sender': '', 'receivers': [''], 'smtphost': '', 'port': '', 'targetUrl': ''}
    # check if file exists
    if not os.path.isfile(configFilename):
        Log.log(Log.error, 'File "{0}" not found. Creating empty config file, please fill in the empty fields'.format(configFilename))
        createEmptyMailconfig(configFilename, defaultConfig)
        return None
    # try loading the config
    with open(configFilename, 'r') as configFile:
        try:
            config = json.load(configFile)
        except json.decoder.JSONDecodeError:
            Log.log(Log.error, 'Corrupt config. Creating empty config file, please fill in the empty fiels')
            createEmptyMailconfig(configFilename, defaultConfig)
            return None
    # check all fields exists
    for key in defaultConfig:
        if not key in config or type(defaultConfig[key]) is not type(config[key]):
            Log.log(Log.error, 'File "mail.config" incomplete. {0} is missing or invalid. Renaming old config file and generating new config'.format(key))
            createEmptyMailconfig(configFilename, defaultConfig)
            return None
    # return valid config
    return config

def createEmptyMailconfig(filename, defaultConfig):
    saveOldMailconfig(filename)
    with open(filename, 'w') as configFile:
        json.dump(defaultConfig, configFile)

def saveOldMailconfig(filename):
    if not os.path.exists(filename):
        return
    targetFileName = '{0}_{1}.json'.format(os.path.splitext(filename)[0], getTimeForFilename())
    if os.path.exists(targetFileName):
        os.remove(targetFileName)
    os.rename(filename, targetFileName)

def sendMail(config, receiver):
    message = """\
From: {sender}
To: {receiver}
Subject: The item you are obeserving is no longer out of stock!

Hi {receiver},

the item you are obeserving on
{url}
is no longer out of stock!

Kind regards
Your out-of-stock parser
""".format(sender = config['sender'], receiver = receiver, url = config['targetUrl'])

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    server = smtplib.SMTP(config['smtphost'], config['port'])
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(config['mailuser'], config['password'])
    server.sendmail(config['sender'], receiver, message)
    Log.log(Log.debug, 'Sucessfully sent mail to {0}'.format(receiver))

def getLogTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getTimeForFilename():
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")

class Log:
    error = 'ERROR'
    info = 'INFO'
    debug = 'DEBUG'

    @staticmethod
    def log(tag, message):
        print('[{time}] [{tag}] {message}'.format(time = getLogTime(), tag = tag, message = message))

if __name__ == "__main__":
    main()
