# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.text import Truncator

from django.contrib.auth.models import User

# Create your models here.


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


#created title of the blog
class Job_Boards(models.Model):
	name = models.CharField(max_length=60, unique=True)
	title  = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('created_at').first()


#created a topic class the handles all topics within the blog
class Job_Topic(models.Model):
	sub_title = models.CharField(max_length=255)
	last_updated = models.DateTimeField(auto_now_add=True)
	board = models.ForeignKey(Job_Boards,related_name='topics')
	starter = models.ForeignKey(User, related_name='topics')
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.sub_title


#created for posting blog post to the database
class Post(models.Model):
	message = models.TextField(max_length=2000)
	topic = models.ForeignKey(Job_Topic, related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='posts')
	updated_by = models.ForeignKey(User, null=True, related_name ='+')

	def __str__(self):
		truncated_message = Truncator(self.message)
		return truncated_message.chars(30)
