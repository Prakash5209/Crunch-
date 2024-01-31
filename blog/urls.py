from django.urls import path

from .views import Home,CreateBlog,BlogDetail,UpdateBlog

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('create-blog/',CreateBlog.as_view(),name="create_blog"),
    path('blog/<int:pk>/',BlogDetail.as_view(),name="blog_detail"),
    path('update-blog/<int:pk>/',UpdateBlog.as_view(),name="update_blog"),
    # path('delete-blog/<int:pk>/',DeleteView.as_view(),name="delete_blog"),
]