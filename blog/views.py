#blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
# Create your views here.

# Next step is to figure out the use cases where remainder_tiles == 1 and == 2
# Also figure the CSS mess

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	posts = posts.reverse()
	post_count = Post.objects.filter(published_date__lte=timezone.now()).count()
	remainder_tiles = post_count % 3
	#fix modulus problem in the templates
	if remainder_tiles == 0:
		return render(request, 'blog/post_list.html', {'posts': posts, 'post_count': post_count})
	else:
		return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)	
	return render(request, 'blog/post_edit.html', {'form': form})









 

