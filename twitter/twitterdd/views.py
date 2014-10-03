from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from twitterdd.models import Tweet, Followers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
import utility
def index(request):
	options = {}
	template = loader.get_template('twitterdd/index.html')
	context = RequestContext(request, options)
	if request.method == 'GET':
		if 'username' in request.session:
			options['login'] = True
			options['logged_in_user'] = request.session['username']
			#get all tweets by chronological order from all people we follow
			options['tweets'] = utility.homepage_tweets(request.session['username'])
	elif request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					options['login'] = True
					options['logged_in_user'] = username
					request.session['username'] = username
					options['tweets'] = utility.homepage_tweets(request.session['username'])
	return HttpResponse(template.render(context))
					

	return HttpResponse(template.render(context))

def userpage(request, username):
	#TAKE INTO ACCOUNT CASE WHEN USER IS NOT LOGGED IN
	options = {}
	template = loader.get_template('twitterdd/user.html')
	context = RequestContext(request, options)
	options['tweets'] = utility.userpage_tweets(username)
	options['username'] = username
	options['num_following'] = utility.num_following(username)
	options['num_follower'] = utility.num_followers(username)
	user1 = User.objects.get(username=username)
	user2 = None
	if 'username' in request.session:
			options['login'] = True
			options['logged_in_user'] = request.session['username']
			user2 = User.objects.get(username=request.session['username'])
			if len(Followers.objects.filter(username1=user1, username2=user2)) == 1:
				options['following'] = True
	#action to follow/unfollow
	if request.method == 'POST':
		if request.POST['action'] == 'follow':
			follow = Followers(username1=user1, username2=user2)
			follow.save()
		else:
			print "user2 is:", user2
			Followers.objects.filter(username1=user1, username2=user2).delete()

	return HttpResponse(template.render(context))
def newuser(request):
	template = loader.get_template('twitterdd/new_user.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def createuser(request):
	#DO VALIDATION CHECKS
	username = request.POST['username']
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	password = request.POST['password']
	email = request.POST['email']
	user = User.objects.create_user(username, email, password, first_name = firstname, last_name = lastname)
	user.save()
	print 'got username', username
	success = True
	if success:
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session['username'] = username
	return redirect('index')

def createsuccess(request, username, password):
	new_user = User.objects.get(username=username)

	options = {}
	options['login'] = True
	options['logged_in_user'] = new_user.username
	user = User.objects.get(username=username)
	login(request, user)
	options['login'] = True
	options['logged_in_user'] = username
	request.session['username'] = username
	template = loader.get_template('twitterdd/index.html')
	context = RequestContext(request, options)
	return HttpResponse(template.render(context))

def user_logout(request):
	print "inside logout"
	logout(request)
	return redirect('index')

def newtweet(request):
	text = request.POST['tweet_text']
	user = User.objects.get(username=request.session['username'])
	tweet = Tweet(username=user, text=text)
	tweet.save()
	return redirect('userpage', request.session['username'])
