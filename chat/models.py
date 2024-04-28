from django.db import models

from account.models import User


#this is temoporary chat
class ChatModel(models.Model):
    me_user = models.ForeignKey(User,on_delete=models.CASCADE)
    other_user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.me_user}-{slef.other_user}"
