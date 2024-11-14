from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from users.models import UserProfile



class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, unique_for_date='created_at', blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')

    def check_is_updated(self):
        return self.updated_at > self.created_at

    def get_absolute_url(self, view_name):
        return reverse(f'blog:{view_name}', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
            ])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def get_absolute_url_delete(self):
        return reverse('blog:comment_delete', args=[self.pk])
