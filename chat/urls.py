from django.urls import path

from chat.views import ChatView,MessageView

app_name = "chat"
urlpatterns = [
    path('',ChatView.as_view(),name="chatview"),
    path('<int:userid>/',MessageView.as_view(),name="MessageView"),
]

