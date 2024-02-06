from django.contrib import admin
from .models import Blog_Category, contact_info,Subscribe, blog_post, Comment



# Register your models here.
admin.site.register(Blog_Category)
admin.site.register(contact_info)
admin.site.register(Subscribe)
admin.site.register(blog_post)
admin.site.register(Comment)