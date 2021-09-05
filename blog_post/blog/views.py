from django.views.generic import ListView, DetailView

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


class PostDetails(DetailView):
    template_name = 'blog/post-details.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['post_tags'] = self.object.tag.all()
        return context
