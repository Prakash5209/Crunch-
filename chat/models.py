from django.db import models

from account.models import User


#this is temoporary chat
class ChatModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    other_chat_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='other_chat_user')
    text = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.other_chat_user}"

    class Meta:
        ordering = ['-created_at']
