from django.db import models


class Tag(models.Model):
    caption = models.CharField(max_length=10)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_add = models.EmailField(max_length=100)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="post")
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default="", null=False, blank=True, unique=True, db_index=True)
    content = models.TextField()
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user_name} {self.post}'
