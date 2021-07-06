import html
import time
import tweepy
import requests
from config import CONSUMER_KEY, ACCESS_TOKEN, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, WEBSITE_URL
from db import DBInstance

db_instance = DBInstance()


def create_api():
    """Create an API object. Make sure you configure the variables in config.py or through environment variables.
    """

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def main():
    previous_links = list(map(lambda x: x[0], db_instance.get_all_posts()))
    while True:
        response = requests.get(f"{WEBSITE_URL}/wp-json/wp/v2/posts/")
        posts_list = response.json()
        unpublished_posts = list(filter(lambda x: x["link"] not in previous_links, posts_list))
        if unpublished_posts:
            print("posts retrieved")

        for new_post in unpublished_posts:
            db_instance.add_post(new_post)
        previous_links.extend(unpublished_posts)

        for post in unpublished_posts:
            title = html.unescape(post["title"]["rendered"])
            if len(title) > 230:
                title = title[0: 230] + "..." + title[-21:]

            link = post["link"]
            time.sleep(1)
            status = f"{title} {link}"
            api.update_status(status)
            time.sleep(60)


api = create_api()
if __name__ == '__main__':
    main()
