from twython import Twython
import json
from pprint import pprint
import time
creds = {"app_key":'', "app_secret":'', "oauth2_token":''}
#######run this to obtain oauth2 token##########
#twitter = Twython(creds['app_key'], creds['app_secret'], oauth_version=2)
#ACCESS_TOKEN = twitter.obtain_access_token() 
################################################


filename = 'C:\Users\Emily\Documents\Classes\CS229\Project\\twittertest3.json'
twitter = Twython(creds['app_key'], access_token=creds['oauth2_token']) #instantiate api 
results = twitter.search(q=['clinton','uranium'], count = 1)

#######run this first to make the json file########
def makeF(filename):
    with open(filename, 'w') as outfile:
    json.dump(results['statuses'], outfile)
    return
####################then run this, get many tweets#########################
def getTweets(filename, fetchN, searchTerms):
    count = 0
    newMax = 1e20
    while True:
        results = twitter.search(q=searchTerms, count = fetchN, max_id=newMax)
        newMax = min([results['statuses'][n]['id'] for n in range(len(results['statuses']))]) - 1
        print "Length of results: ", len(results['statuses'])
        print "Min ID - 1: ", newMax
        print "count: ", count
        for n in range(len(results['statuses'])):
            with open (filename, mode="r+") as file:
                file.seek(0,2)
                position = file.tell() -1
                file.seek(position)
                file.write( ",{}]".format(json.dumps(results['statuses'][n])))
        count+=fetchN
        if count > 450:
            print "sleeping..."
            time.sleep(1000)
            count = 0    
    return
    
############read json file#############
def rF(filename):
    with open(filename, 'r') as f:
        mydata = json.load(f)
    return mydata

getTweets(filename, 15,['clinton','uranium'])

#def main():
#    return
#if __name__ == '__main__':
#    main()