from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .forms import CommentForm
from .models import Post


class StartingPage(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-date')[:3]

    context_object_name = 'posts'


class PostsList(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'


class PostDetails(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blog/post-details.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('single-post', args=[slug]))

        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id')
        }
        return render(request, 'blog/post-details.html', context)
