from django.contrib import admin
from .models import UserProfile, Post


admin.site.register(UserProfile)

@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('title', 'create_at')
    prepopulated_fields = {
        'slug': ('title',)
    }
