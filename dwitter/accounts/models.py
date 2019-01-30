# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm # new

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=10, unique=True)
	pin = models.IntegerField()
	follower = models.ManyToManyField("self", symmetrical=False, null=True)
	def __str__(self):
		return self.username


class Comment(models.Model):
	comment = models.CharField(max_length=120)

	def __str__(self):
		return "%s" % (self.comment)


class Like(models.Model):
	liker = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % (self.liker)

class Dweet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=150)
	comments = models.ManyToManyField(Comment, symmetrical=False)
	likes = models.ManyToManyField(Like, symmetrical=False)

	def __str__(self):
		return "%s | %s" % (self.user, self.content)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'pin']

class DweetForm(ModelForm):
	class Meta:
		model = Dweet
		fields = ['content']

class CommentFrom(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']
