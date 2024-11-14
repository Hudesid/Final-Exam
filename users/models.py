import uuid
from django.conf import settings
from django.db import models



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