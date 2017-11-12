#==============================================================================
# get tweets corresponding to a search query
# I slightly modified 
# https://medium.com/@dawran6/twitter-scraper-tutorial-with-python-requests-beautifulsoup-and-selenium-part-2-b38d849b07fe
#==============================================================================
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='

query = u'clinton' 
url = base_url + query

browser.get(url)
time.sleep(1)

body = browser.find_element_by_tag_name('body')

for _ in range(1):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

tweets = browser.find_elements_by_class_name('tweet')

for tweet in tweets:
    print 'tweet id: ', tweet.get_attribute('data-tweet-id')
    print 'json: ', tweet.get_attribute('data-reply-to-users-json')
    print 'user id: ', tweet.get_attribute('data-user-id')
    print 'data-permalink-path: ', tweet.get_attribute('data-permalink-path')
    print 'data-conversation-id: ', tweet.get_attribute('data-conversation-id')
    print 'data-screen-name: '. tweet.get_attribute('data-screen-name')

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