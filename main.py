import html
import os
import time

import tweepy
import json
import requests
from config import CONSUMER_KEY, ACCESS_TOKEN, CONSUMER_SECRET, ACCESS_TOKEN_SECRET


def create_api():
    """Create an API object. Make sure you configure the variables in config.py or through environment variables.
    """

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#
api = create_api()

while True:
    previous_links = []
    with open(os.path.join(os.getcwd(), "assets/previous_links.txt"), 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]
            previous_links.append(currentPlace)


    response = requests.get("https://almostfree.me/wp-json/wp/v2/posts/")
    posts_list = response.json()
    unpublished_posts = list(filter(lambda x: x["link"] not in previous_links, posts_list))

    with open("assets/previous_links.txt", 'w') as filehandle:
        for listitem in posts_list:
            filehandle.write('%s\n' % listitem["link"])

    for post in unpublished_posts:
        title = html.unescape(post["title"]["rendered"])
        link = post["link"]
        time.sleep(1)
        api.update_status(f"Check out this new article{title} {link}")
        time.sleep(60)
