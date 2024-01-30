from django.urls import path
from account import views

app_name = "account"
urlpatterns = [
    path('login/',views.userLogin,name="userLogin"),
    path('signup/',views.userSignup,name="userSignup"),
    path('logout/',views.userLogout,name='userLogout'),
]