from django.db import models
from django.conf import settings

class CreateBlogModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} --------by -{self.user}"
    

# class LikeModel(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     createblogmodel_id = models.ForeignKey(CreateBlogModel,on_delete=models.CASCADE)
#     like_count = models.BooleanField(True)