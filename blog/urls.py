from django.urls import path

from blog.views import Home,CreateBlog,BlogDetail,UpdateBlog,Aboutpage,Contactpage,DeleteBlog,search_feature,like_post,DeleteComment,rateBlog,LinkContainer,NotificationView

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('create-blog/',CreateBlog.as_view(),name="create_blog"),
    path('like-post/<str:slug>/',like_post,name='like_post'),
    path('blog/<str:slug>/',BlogDetail,name="blog_detail"),
    path('update-blog/<str:slug>/',UpdateBlog.as_view(),name="update_blog"),
    path('search/',search_feature,name='search_feature'),
    path('delete-blog/<int:pk>/',DeleteBlog.as_view(),name="delete_blog"),
    path('about-us/',Aboutpage.as_view(),name='Aboutpage'),
    path('contact-us/',Contactpage.as_view(),name='Contactpage'),
    path('rate-blog/<str:slug>/',rateBlog,name="rateBlog"),
    path('save-link/<int:pk>/',LinkContainer,name="save_link"),

    path('notification/',NotificationView.as_view(),name='notification'),

    path('delete-comment/<int:pk>/',DeleteComment,name="DeleteComment"),
]
