!pip install snscrape
!pip install git+https://github.com/JustAnotherArchivist/snscrape.git

import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data
list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
def snt(keyword, since, until, count):
    for i, tweet in enumerate('{0} since:{1} until:{2}'.format(keyword, since, until)):
        if i > count:
            break
        list.append([tweet.date, tweet.id, tweet.content])

    # Creating a dataframe from the tweets list above
    list = pd.DataFrame(list, columns = ['Datetime', 'Tweet Id', 'Text'])
