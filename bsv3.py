#==============================================================================
# get tweets corresponding to a search query
# I slightly modified 
# https://medium.com/@dawran6/twitter-scraper-tutorial-with-python-requests-beautifulsoup-and-selenium-part-2-b38d849b07fe
#==============================================================================
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
        print count
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

searchTwitter('clinton',10,25,'testA.json')
myD = rF('testA.json')
print len(myD)

def makeLabeled(filename, startInd, endInd):
    dat = rF(filename)    
    for entry in dat[startInd:endInd]:
        print entry['tweet-all']
        trueFalse = raw_input("1 = fake news, 0 = true news, 5 = other/opinion ")
        ## 1 = FN, 0 = TN, 5 = other
        entry['FN'] = trueFalse
        print entry['FN']    
    makeF('labeled' + filename, dat)

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