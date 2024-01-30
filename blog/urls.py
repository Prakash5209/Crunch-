from django.urls import path

from .views import Home,CreateBlog

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('create-blog/',CreateBlog.as_view(),name="create_blog"),
]