from django.db import models
from django.conf import settings
from django.urls import reverse


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/')
    create_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=255, unique_for_date='create_at')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.create_at.year,
            self.create_at.month,
            self.create_at.day,
            self.slug
            ])

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)