import tweepy
import requests
import os
import pandas as pd
from creds import api_key, api_secret, access_token, access_token_secret

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

#TODO: Set keyword properly, should I be using graph?
query = 'alttext filter:images'

MAX_TWEETS = 1000000

download_dir = 'alttext'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
rows = []
tweets = tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended', lang='en').items(MAX_TWEETS)
# tweets = api.user_timeline(screen_name='Barchart', count=10000, tweet_mode='extended')
for tweet in tweets:
    if 'extended_entities' in tweet._json:
        media_entities = tweet._json['extended_entities']['media']
        for media in media_entities:
            if media['type'] == 'photo':
                image_url = media['media_url']
                image_filename = os.path.join(download_dir, f'{tweet.id}.jpg')
                response = requests.get(image_url, stream=True)
                with open(image_filename, 'wb') as image_file:
                    for chunk in response.iter_content(1024):
                        image_file.write(chunk)
                caption = tweet.full_text
                tweet_url = media['url']
                picture_url = media['media_url_https']
                created_at = tweet.created_at
                alt_text = None
                if 'ext_alt_text' in media:
                    alt_text = media['ext_alt_text']
                elif 'description' in media:
                    alt_text = media['description']
                if alt_text:
                    print(alt_text)
                row = [f'{tweet.id}.jpg', caption, tweet_url, picture_url, created_at, alt_text]
                rows.append(row)
#                 # print('Downloaded image: {} Caption: {} Alt-text: {}'.format(image_filename, caption, alt_text))
#
#
print('Image crawling complete!')
df = pd.DataFrame(rows)
df.to_csv(f'{download_dir}/{download_dir}.csv', sep=',', index=False, header=['image_filename', 'caption', 'tweet_url',
                                                                              'picture_url','created_at','alt_text'])
#
