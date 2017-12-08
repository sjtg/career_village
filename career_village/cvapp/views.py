# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Post
# Create your views here.


def home(request):
	homes = cvapp.objects.all()
	return render(request, 'home.html', {'homes': homes})
