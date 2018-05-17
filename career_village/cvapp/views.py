from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Photo
from .forms import PhotoForm
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .forms import NewTopicForm, PostForm

from .models import Job_Boards, Job_Topic, Post

from django.db.models import Count

from .filters import UserFilter
# Create your views here.

#Home page Career Village
def home(request):
	jobs_lists = Photo.objects.all()
	boards = Job_Boards.objects.all()
	return render(request, 'web/index.html', {'photos': jobs_lists, 'boards': boards})


#upload and crop function
class dashboardView(View):
    def get(self, request):
	        jobs_lists = Photo.objects.all()
	        return render(self.request, 'web/dashboard.html', {'photos': jobs_lists})

    def post(self, request):
        #time.sleep(1)
		form = PhotoForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			    #photo = request.user
	          	    photo = form.save()
		    	    photo.uploaded_at = timezone.now()
	                    data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
		else:
		        data = {'is_valid': False}
		return JsonResponse(data)


#created

#created topics function to list the topics within the board
def topics(request, pk):
	board = get_object_or_404(Job_Boards, pk=pk)
	topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
	return render(request, 'web/topics.html', {'board':board, 'topics' : topics})


#created new topic function, this will show  new topics in the dashboard
@login_required
def new_topics(request, pk):
	board = get_object_or_404(Job_Boards, pk=pk)
	#user = User.objects.first()

	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()
			Post.objects.create(
				message = form.cleaned_data.get('message'),
				topic = topic,
				created_by = request.user
			)

			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()

	return render(request, 'web/new_topics.html', {'board' : board, 'form':form })


def topic_posts(request, pk, topic_pk):
	topic = get_object_or_404(Job_Topic, board__pk=pk, pk=topic_pk)
	topic.views += 1
	topic.save()
	return render(request, 'web/topic_posts.html', {'topic' : topic})


@login_required
def reply_topic(request, pk, topic_pk):
	topic = get_object_or_404(Job_Topic, board__pk=pk, pk=topic_pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = request.user
			post.save()
			return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
	else:
		form = PostForm()
	return render(request, 'web/reply_topic.html', {'topic' : topic, 'form':form})


#created a search function
def search(request):
	user_list = User.objects.all()
	user_filter = UserFilter(request.GET, queryset=user_list)
	jobs_lists = Job_Topic.objects.all()
	jobs_filter = JobFilter(request.GET, queryset=jobs_lists)
	return render(request, 'web/index.html', {'filter': user_filter, 'filter' : jobs_filter})
