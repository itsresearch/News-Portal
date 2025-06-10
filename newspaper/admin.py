from django.contrib import admin
from newspaper.models import Category, Post, Tag, Advertisement, UserProfile, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category) 
admin.site.register(Advertisement)
admin.site.register(UserProfile) 
admin.site.register(Comment) 


