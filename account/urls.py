from django.urls import path
from account import views

from .views import ViewProfile,FollowInProfile,UpdateProfile

app_name = "account"
urlpatterns = [
    path('login/',views.userLogin,name="userLogin"),
    path('profileview/<int:pk>/',ViewProfile.as_view(),name="ProfileView"),
    path('update-profile/<int:pk>/',UpdateProfile.as_view(),name="UpdateProfile"),
    path('follow-in-profile/<int:pk>/',FollowInProfile.as_view(),name="followInProfile"),
    path('signup/',views.userSignup,name="userSignup"),
    path('logout/',views.userLogout,name='userLogout'),
]