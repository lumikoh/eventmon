import requests
import json

def getFromLocation(url):
    response_API = requests.get(url)
    data = response_API.text
    return json.loads(data)
    

def getScriptsFromFile(path):
    file = open(path, 'r')
    commands = file.read().strip('\n').split(';')
    file.close()
    del commands[-1]
    return commands