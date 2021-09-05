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

    def is_stored_post(self, request, post_id):
        stored_post = request.session.get('stored_posts')
        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            'post': post,
            'post_tags': post.tag.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_post(request, post.id)
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
            'comments': post.comments.all().order_by('-id'),
            'saved_for_later': self.is_stored_post(request, post.id)
        }
        return render(request, 'blog/post-details.html', context)


class ReadLaterView(View):

    def get(self, request):
        stored_post = request.session.get('stored_posts')

        context = {}
        if stored_post is None or len(stored_post) == 0:
            print('here')
            context['posts'] = []
            context['has_post'] = False

        else:
            posts = Post.objects.filter(id__in=stored_post)
            context['posts'] = posts
            context['has_post'] = True

        return render(request, 'blog/stored-posts.html', context)

    def post(self, request):
        stored_post = request.session.get('stored_posts')
        if stored_post is None:
            stored_post = []

        post_id = int(request.POST['post_id'])
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session['stored_posts'] = stored_post

        return HttpResponseRedirect('/')
