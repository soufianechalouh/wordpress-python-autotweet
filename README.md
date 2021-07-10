# wordpress-python-autotweet
This script does what it says: Automate publishing new Wordpress blog posts in twitter.

To avoid twitter ban, it publishes a maximum of 1 tweet every 60 seconds. You can edit that from the main file.
##How to use it:
- Sign up for [Twitter API](https://developer.twitter.com/) with the accounts you want to publish from

- Make sure that REST is enabled on your wordpress blog by adding "/wp-json/wp/v2/posts/" to your website url

- Configure this project from config.py file

- Run main.py

