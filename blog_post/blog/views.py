from django.shortcuts import render, get_object_or_404

from .models import Post


def get_date(post):
    return post['date']


def starting_page(request):
    latest_post = Post.objects.all().order_by("-date")[:3]
    # sorted_post = sorted(all_posts, key=get_date)
    # latest_post = sorted_post[-3:]

    return render(request, "blog/index.html", {
        "posts": latest_post
    })


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })


def post_details(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-details.html", {
        "post": identified_post,
        "post_tags": identified_post.tag.all()
    })
