from django.urls import path
from account import views

from .views import ViewProfile,FollowInProfile,UpdateProfile,Library,search_feature_library,DeleteBlog_library,Forgot_password

app_name = "account"
urlpatterns = [
    path('login/',views.userLogin,name="userLogin"),
    path('profileview/<int:pk>/',ViewProfile.as_view(),name="ProfileView"),
    path('update-profile/<int:pk>/',UpdateProfile.as_view(),name="UpdateProfile"),
    path('follow-in-profile/<int:pk>/',FollowInProfile.as_view(),name="followInProfile"),
    path('signup/',views.userSignup,name="userSignup"),
    path('logout/',views.userLogout,name='userLogout'),

    path('library/',Library.as_view(),name="Library"),
    path('search-library/',search_feature_library,name='search_feature_library'),
    path('delete-blog/<int:pk>/',DeleteBlog_library.as_view(),name="DeleteBlog_library"),

    path('forgot-password/',Forgot_password.as_view(),name="Forgot_password"),
]
