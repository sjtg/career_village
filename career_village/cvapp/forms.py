from django.core.files import File
from django import forms
from .models import *

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title','file', )



class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': "What's on your mind?"}
		),
		max_length=5000)

	class Meta:
		model= Job_Topic
		fields = ['sub_title', 'message']


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['message', ]
