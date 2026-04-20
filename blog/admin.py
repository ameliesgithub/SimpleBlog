from django.contrib import admin

from blog.models import Category, Post, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(UserProfile)


