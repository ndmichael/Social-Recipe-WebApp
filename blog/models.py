from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

'''
    Post model for the blog
'''
class Post(models.Model):
    STATUS_POST = (
        ('published', 'Published'),
        ('status', 'Status'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_POST, default='published')
    likes = models.ManyToManyField(User, default=None, related_name='user_like', blank=True)
    like_count = models.BigIntegerField(default="0")
    slug = models.SlugField(max_length=150,)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', default="",  blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):  # i override the save method to prepopulate slugs, another way is using signals
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk, 'year': self.date_created.year, 'title': self.slug})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.post}")











