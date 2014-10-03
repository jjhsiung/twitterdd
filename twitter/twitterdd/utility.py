from twitterdd.models import Tweet, Followers
from django.contrib.auth.models import User

def homepage_tweets(username):
	user = User.objects.get(username=username)
	following = Followers.objects.filter(username2=user).values('username1')
	ids = []
	for f in following:
		ids.append(f['username1'])
	return Tweet.objects.filter(username__pk__in=ids).order_by('-timestamp')

def userpage_tweets(username):
	user = User.objects.get(username=username)
	return Tweet.objects.filter(username=user).order_by('-timestamp')

def num_followers(username):
	user = User.objects.get(username=username)
	return len(Followers.objects.filter(username1=user))
def num_following(username):
	user = User.objects.get(username=username)
	return len(Followers.objects.filter(username2=user))