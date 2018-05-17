from django.contrib.auth.models import User
from .models import  Job_Boards
import django_filters



class UserFilter(django_filters.FilterSet):
	class Meta:
		model = User
		fields = ['username',   ]

# class JobFilter(django_filters.FilterSet):
#     class Meta:
#         model = Job_Topic
#         fields = ['title', ]
