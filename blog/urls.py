from django.urls import path

from blog.views import Home,CreateBlog,BlogDetail,UpdateBlog

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('create-blog/',CreateBlog.as_view(),name="create_blog"),
    path('blog/<int:pk>/',BlogDetail,name="blog_detail"),
    # path('blog/<int:pk>/comment/',Blog_Comment.as_view(),name="comment_blog"),  
    path('update-blog/<int:pk>/',UpdateBlog.as_view(),name="update_blog"),
    # path('delete-blog/<int:pk>/',DeleteView.as_view(),name="delete_blog"),
]