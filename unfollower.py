#!/usr/bin/env python3

#need to install twitter api: 'sudo pip install twitter'
import twitter
import os
import urllib.request
import time
import calendar

def auth():
	MY_TWITTER_CREDS = os.path.expanduser('~/.twitter')
	APP_NAME = 'unfollower'
	CONSUMER_KEY = input('Input consumer key:')
	CONSUMER_SECRET = input('Input consumer secret:')
	if not os.path.exists(MY_TWITTER_CREDS):
		print('oauth dance...')
		twitter.oauth_dance(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

	oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)
	print('auth...')
	t = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

	return t


def unfollow(raw_ids):
	for uid in raw_ids['ids']:
		print(uid)
		twts = t.statuses.user_timeline(user_id = uid, count = 1)
		print(len(twts))
		time.sleep(2)

		if len(twts)<1 or time.time()-calendar.timegm(time.strptime(twts[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')) > 2000000 :
			uf = t.friendships.destroy(user_id=uid)
			time.sleep(2)
			print('unfollowing {0}...'.format(uf['name']))


if __name__ == '__main__':
	#need proxy to open twitter in China
	proxy_handler = urllib.request.ProxyHandler({'https': 'http://127.0.0.1:8123/'})
	opener = urllib.request.build_opener(proxy_handler)
	urllib.request.install_opener(opener)
	
	t = auth()
	raw_ids = t.friends.ids(count=5000)
	#print(raw_ids)
	unfollow(raw_ids)


