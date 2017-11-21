#==============================================================================
# get tweets corresponding to a search query
# I slightly modified 
# https://medium.com/@dawran6/twitter-scraper-tutorial-with-python-requests-beautifulsoup-and-selenium-part-2-b38d849b07fe
#==============================================================================
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

def searchTwitter(query, num_pages, totLoops, filename):
    browser = webdriver.Chrome()
    base_url=u'https://twitter.com/search?f=tweets&vertical=news&q='
#    base_url = u'https://twitter.com/search?q='
#query = u'clinton' 
    url = base_url + query
    
    browser.get(url)
    time.sleep(1)
    
    body = browser.find_element_by_tag_name('body')
    
    count = 0
    tweet_ids = {}
    while count < totLoops:
        for _ in range(num_pages):#count*num_pages, (count+1)*num_pages): ##
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        
        tweets = browser.find_elements_by_class_name('tweet')
        dictList = []
        for tweet in tweets:
            tweet_id = tweet.get_attribute('data-tweet-id')
            if tweet_id in tweet_ids:
                continue
            else:
                dictList.append(makeTweetDict(browser, tweet))
                tweet_ids[tweet_id] = True
        makeF(filename, dictList)   
        print(count)
        count+=1        
    return 

def searchTwitterUser(user, num_pages, totLoops, filename):
    browser = webdriver.Firefox()
    base_url=u'https://twitter.com/'
#    base_url = u'https://twitter.com/search?q='
#query = u'clinton' 
    url = base_url + user
    
    browser.get(url)
    time.sleep(1)
    
    body = browser.find_element_by_tag_name('body')
    
    count = 0
    tweet_ids = {}
    while count < totLoops:
        for _ in range(num_pages):#count*num_pages, (count+1)*num_pages): ##
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        
        tweets = browser.find_elements_by_class_name('tweet')
        dictList = []
        for tweet in tweets:
            tweet_id = tweet.get_attribute('data-tweet-id')
            if tweet_id in tweet_ids:
                continue
            else:
                dictList.append(makeTweetDict(browser, tweet))
                tweet_ids[tweet_id] = True
        makeF(filename, dictList)   
        print(count)
        count+=1        
    return 


def makeTweetDict(browser, tweet):
    tweetDict = {}
    tweet_id = tweet.get_attribute('data-tweet-id')

    try:
        tweetText = browser.find_element_by_xpath('//*[@id="stream-item-tweet-{}"]//p'.format(str(tweet_id))).text        
    except:
        tweetText = None
    try:
        timeStamp = browser.find_element_by_xpath('//*[@id="stream-item-tweet-{}"]//small/a'.format(str(tweet_id))).get_attribute('title')
    except:
        timeStamp = None
     
    try: 
        cut= tweet.text[tweet.text.find('\nReply\n'):len(tweet.text)]
        replies = cut.split('\n')[2]; retweets = cut.split('\n')[4]; likes = cut.split('\n')[6]
    except:
        replies = None; retweets = None; likes = None
 
    tweetDict['tweet-text'] = tweetText
    tweetDict['timestamp'] = timeStamp
    tweetDict['data-tweet-id'] = tweet_id 
    tweetDict['data-reply-to-users-json'] = tweet.get_attribute('data-reply-to-users-json')
    tweetDict['data-user-id'] = tweet.get_attribute('data-user-id')
    tweetDict['data-permalink-path'] = tweet.get_attribute('data-permalink-path')
    tweetDict['data-conversation-id'] = tweet.get_attribute('data-conversation-id')
    tweetDict['data-screen-name'] = tweet.get_attribute('data-screen-name')
    tweetDict['data-is-reply-to'] = tweet.get_attribute('data-is-reply-to')
    tweetDict['tweet-all'] = tweet.text
    tweetDict['replies'] = replies
    tweetDict['retweets'] = retweets
    tweetDict['likes'] = likes
    tweetDict['data-mentions'] = tweet.get_attribute('data-mentions')
    
    return tweetDict
    

def makeF(filename, dictList):
    try:
        for n in range(len(dictList)):
            with open (filename, mode="r+") as outfile:
                outfile.seek(0,2)
                position = outfile.tell() -1
                outfile.seek(position)
                outfile.write( ",{}]".format(json.dumps(dictList[n])))                   
    except:
        with open(filename, 'w') as outfile:
            json.dump(dictList, outfile)
    return
        
############read json file#############
def rF(filename):
    with open(filename, 'r') as f:
        mydata = json.load(f)
    return mydata



def makeLabeled(filename,folder, startInd, endInd):
    dat = rF(folder+filename)    
    for entry in dat[startInd:endInd]:
        print(entry['tweet-all'])
        trueFalse = input("1 = fake news, 0 = true news, 5 = other/opinion ")
        ## 1 = FN, 0 = TN, 5 = other
        entry['FN'] = trueFalse
        print(entry['FN'])
    makeF(folder + 'labeled' + filename, dat[startInd:endInd])
    
def main():
    folder = 'Data/'
    
    filename = 'brexit2017_3_30-2017_3_31.json'
    #user = 'realDonaldTrump'
    
    #searchTwitterUser(user,5,500,folder+filename)
    search_date = datetime.date(2017,1,1)
    
    for i in range(30):
        search_date_po = search_date.replace(day = search_date.day + 1)
        #query = 'brexit until:2017-03-31 since:2017-03-30'
        filename = 'brexit'+search_date_po.strftime('%Y_%m_%d')+'-'+search_date.strftime('%Y_%m_%d')
        query = 'brexit until:'+search_date_po.strftime('%Y-%m-%d')+' since:'+search_date.strftime('%Y-%m-%d')
        print('Querying:')
        print(query)
        print('\n')
        searchTwitter(query,5,50,folder+filename)
        search_date = search_date.replace(day = search_date.day + 1)

    #makeLabeled(filename, folder, 0, 10)


if __name__ == '__main__':
    main()
    



#==============================================================================
# get tweet info from particular url
#==============================================================================
#import requests
#from bs4 import BeautifulSoup
#
#url = "https://twitter.com/nokia"
#response = requests.get(url)
#soup = BeautifulSoup(response.text,"lxml")
#tweets = soup.findAll('li',{"class":'js-stream-item'})
#for tweet in tweets:
#    if tweet.find('p',{"class":'tweet-text'}):
#        tweet_user = tweet.find('span',{"class":'username'}).text.strip()
#        tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
#        replies = tweet.find('span',{"class":"ProfileTweet-actionCount"}).text.strip()
#        retweets = tweet.find('span', {"class" : "ProfileTweet-action--retweet"}).text.strip()
#        print(tweet_user)
#        print(tweet_text)
#        print(replies)
#        print(retweets)
#    else:
#        continue

###### get total number of followers of user ##########
#from bs4 import BeautifulSoup
#import requests
#username='justinbieber'
#url = 'https://www.twitter.com/'+username
#r = requests.get(url)
#soup = BeautifulSoup(r.content)
#
#f = soup.find('li', class_="ProfileNav-item--followers")
#title = f.find('a')['title']
#print title
## 81,346,708 Followers
#
#num_followers = int(title.split(' ')[0].replace(',',''))
#print num_followers