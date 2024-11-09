import uuid

from django.db import models
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


class UserProfile(models.Model):
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.jpg',
        blank=True
    )
    is_verified_email = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def __str__(self):
        return self.user.username


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

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
            ])

    def get_absolute_url_2(self):
        return redirect(reverse('blog:post_detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
            ]))

    def get_absolute_url_update(self):
        return redirect(reverse('blog:post_update', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ]))

    def get_absolute_url_delete(self):
        return reverse('blog:post_delete', args=[
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

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

class UserToken(models.Model):
    token = models.CharField(max_length=500, unique=True, blank=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='token')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)