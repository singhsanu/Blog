"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from myblog import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('blog',views.blog,name='blog'),
    path('sub',views.sub,name='Subscribe'),
    path('ck',views.ck,name='ck'),
    path('allblogs',views.allblogs,name='allblogs'),
    path('blog_details/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('blog_cat/<str:blog_cat>/', views.blog_cat, name='blog_cat'),
    path('loginuser',views.loginuser,name='loginuser'),
    path('signupuser',views.signupuser,name='signupuser'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('search',views.search,name='search'),
    path('add_like/<int:blog_id>/', views.add_like, name='add_like'),
    path('add_comment/<int:blog_id>/',views.add_comment, name='add_comment'),
    path('delete_comment/<int:blog_id>/<int:comment_id>/',views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:blog_id>/<int:comment_id>/',views.edit_comment, name='edit_comment'),


    


]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
