from django.db import models
from tinymce import models as tinymce_models
from django.conf import settings

class Status(models.TextChoices):
    DRAFT = 'draft','DRAFT',
    PUBLIC = 'public','PUBLIC',

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CreateBlogModel(TimeStampModel):
    image = models.ImageField(upload_to='post',blank=True,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField()
    status = models.CharField(max_length=255,choices=Status.choices,default=Status.DRAFT)

    
    def __str__(self):
        return f'title:{self.title}, by:{self.user}'
    
class BlogCommentModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    blog_id = models.ForeignKey(CreateBlogModel,on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self',null = True,blank = True,on_delete=models.CASCADE,related_name = 'replies')
    comment = models.TextField()

    def __str__(self):
        return f'user:{self.user}, post_id:{self.blog_id}, comment:{self.comment[:30]}...'


# class LikeModel(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     createblogmodel_id = models.ForeignKey(CreateBlogModel,on_delete=models.CASCADE)
#     like_count = models.BooleanField(True)