from django.urls import path

from blog.views import Home,CreateBlog,BlogDetail,UpdateBlog,Aboutpage,Contactpage,DeleteBlog

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('create-blog/',CreateBlog.as_view(),name="create_blog"),
    path('blog/<int:pk>/',BlogDetail,name="blog_detail"),
    # path('blog/<int:pk>/comment/',Blog_Comment.as_view(),name="comment_blog"),  
    path('update-blog/<int:pk>/',UpdateBlog.as_view(),name="update_blog"),
    path('delete-blog/<int:pk>/',DeleteBlog.as_view(),name="delete_blog"),
    path('about-us/',Aboutpage.as_view(),name='Aboutpage'),
    path('contact-us/',Contactpage.as_view(),name='Contactpage')
]