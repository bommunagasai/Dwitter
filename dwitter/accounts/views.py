# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from models import UserForm, User, Dweet, DweetForm, CommentFrom, Comment, Like
from rest_framework import filters

# Create your views here.
def home(request):
	if request.session.has_key('username') and request.session.has_key('pin'):
		return redirect("http://127.0.0.1:8000/accounts/")
	else:
		context_dict = {'username': '', 'pin': ''}
		return redirect("http://127.0.0.1:8000/accounts/login/")

def login(request):
	flag = False
	if request.method == 'POST':
		form = UserForm(request.POST)

		try:
			user = User.objects.get(username =  request.POST['username'])

			if user:
				print(user.pin)
				if user.pin == int(form['pin'].value()):
					request.session['username'] = request.POST['username']
					request.session['pin'] = request.POST['pin']
					flag = True
					print(request.POST['username'] +"|" + request.POST['pin'])
					return redirect("http://127.0.0.1:8000/accounts/")
		except User.DoesNotExist:
			user = None

	return render(request, 'login.html', {'form': UserForm()})

	

def signup(request):

	if request.method == 'POST':
		form = UserForm(request.POST)
		print(form['username'].value())
		print form.is_valid()
		if form.is_valid():
			user = User()
			user.username = form['username'].value()
			user.pin = form['pin'].value()
			user.save()
			request.session['username'] = request.POST['username']
			request.session['pin'] = request.POST['pin']
			SESSION_COOKIE_AGE = 30
			return redirect("http://127.0.0.1:8000/dweets/")

	return render(request, 'signup.html', { 'form': UserForm() })

def logout(request):
	key_variable = request.session.pop('pin')
	return redirect("http://127.0.0.1:8000/")

from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework.decorators import action, detail_route

class DweetViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.DweetSerializer
	queryset = Dweet.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ('content',)

	
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @detail_route(methods=['post','get'])
    def dweets(self, request, pk=None):
    	if request.method == 'POST':
    		form = DweetForm(request.POST)
    		if form.is_valid():
    			dweet = Dweet()
    			dweet.content = request.POST['content']
    			dweet.user = User.objects.filter(username = self.get_object())[0]
    			dweet.save()

    	uid = User.objects.filter(username = self.get_object())[0]
    	dwts = Dweet.objects.filter(user_id = uid.id)
    	#print(dwts)
    	serializer = serializers.AccountSerializer
    	return render(request, 'dweets.html',{ 'form': DweetForm(), 'username': self.get_object(), 'dwts': dwts })


    @detail_route(methods=['get'])
    def follow(self, request, *args, **kwargs):
    	#print("##########################")
    	#print(request.GET["user_id"])
    	u2 = User.objects.filter(username = self.get_object())[0]
    	follower_1 = User.objects.get(id = request.GET["user_id"])
    	if request.method == 'GET':
    		u2.follower.add(follower_1)
    	return 	redirect("http://127.0.0.1:8000/accounts/users/"+str(u2.id)+"/feed")

    @detail_route(methods=['get'])
    def unfollow(self, request, *args, **kwargs):
    	u2 = User.objects.filter(username = self.get_object())[0]
    	follower_1 = User.objects.get(id = request.GET["user_id"])
    	if request.method == 'GET':
    		u2.follower.remove(follower_1)
    	return 	redirect("http://127.0.0.1:8000/accounts/users/"+str(u2.id)+"/feed")

    @detail_route(methods=['get','post'])
    def feed(self, request, *args, **kwargs):
    	u2 = User.objects.filter(username = self.get_object())[0]
    	followers = u2.follower.all()
    	dwts = []

    	if request.method == 'POST' and 'btn_comment' in request.POST:
    		c = Comment()
    		c.comment = request.POST['comment']
    		# print()
    		# print(request.POST['comment'])
    		# print()
    		# print()
    		c.save()
    		dweet = Dweet.objects.get(id = request.POST['dweet_id'])
    		dweet.comments.add(c)
    	elif request.method == 'POST' and 'btn_like' in request.POST:
    		u = User.objects.filter(username = self.get_object())[0]
    		dweet = Dweet.objects.get(id = request.POST['dweet_id'])
    		#print(dweet.likes.filter(liker = u).count())
    		if dweet.likes.filter(liker = u).count() == 0:
    			#print('like create')
	    		l = Like()
	    		u = User.objects.filter(username = self.get_object())[0]
	    		l.liker = u
	    		l.save()
	    		dweet = Dweet.objects.get(id = request.POST['dweet_id'])
	    		dweet.likes.add(l)

    	for f in followers:
    		d = Dweet.objects.filter(user = f).all()
    		# d.comments = d.comments.all()
    		#print(d)
    		dwts.append(d)

    	return render(request, 'feed.html',{ 'username': self.get_object(), 'dwts': dwts, 'form': CommentFrom() })


