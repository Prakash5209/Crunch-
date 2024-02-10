from django.urls import path
from account import views

from .views import ViewProfile

app_name = "account"
urlpatterns = [
    path('login/',views.userLogin,name="userLogin"),
    path('profileview/<int:pk>/',ViewProfile.as_view(),name="ProfileView"),
    path('signup/',views.userSignup,name="userSignup"),
    path('logout/',views.userLogout,name='userLogout'),
]