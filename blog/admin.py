from django.contrib import admin
from .models import Post, Comment, UserProfile, UserLikes


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(UserLikes)


