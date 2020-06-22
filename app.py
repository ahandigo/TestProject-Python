from flask import Flask, request
import json
from tinydb import TinyDB
from tinydb import Query

app = Flask(__name__)
db = TinyDB('db.json') #current apps on the user's phone and their versions
store = TinyDB('store.json') #mock data for all apps available in the play store
result = TinyDB('result.json') #stores all the apps that need to be updated


@app.route('/current', methods=['GET'])
def get_app_versions(): #gets the current apps and their versions
     print(f'Request: {request}')
     return json.dumps({"Current Apps": db.all()})


def get_updates(): #gets the updates that needs to be made
    for i in db: #iterates through the current apps database
        curID = db[i].appID #finds the app ID of the ith document (or app)
        b = Query() #sets up a query to search for the current app ID in the store
        c = store.search(b.appID == curID) #searches for a matching app ID
        #compares the versions of the app from the store and the app that the user currently has
        #to see if a new version is needed
        #if a newer version is found, and the OS of the current app can support the new app,
        #inserts it into the result
        if ((c.version > db[i].version) & (c.OS == db[i].OS)):
            result.insert(c)




@app.route('/updates', methods=['GET'])
def get_app_updates():
    print(f'Request: {request}')
    #the result database composed of jsons of the needed updates is returned
    #by the web server when the android end sends a get request
    return json.dumps({"Updates": result.all()})


if __name__ == '__main__':
    app.run()

