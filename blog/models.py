from django.db import models
from tinymce import models as tinymce_models
from django.conf import settings
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.utils import timezone
from django.utils.text import slugify

from account.models import User


class Status(models.TextChoices):
    DRAFT = 'draft', 'DRAFT',
    PUBLIC = 'public', 'PUBLIC',

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-modified_at', '-created_at']

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

class CreateBlogModel(TimeStampModel):
    image = models.ImageField(upload_to='post', blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_username')
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField()
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.DRAFT)
    tags = TaggableManager()
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'title:{self.title}, by:{self.user}'

class BlogCommentModel(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(
        CreateBlogModel, on_delete=models.CASCADE, related_name='blog_comment')
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user}{self.comment}'


class LikeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(
        CreateBlogModel, on_delete=models.CASCADE, related_name="blog_like")

    def __str__(self):
        return str(self.id)


class Rating(models.Model):
    rate = models.IntegerField()
    blog = models.ForeignKey(
        CreateBlogModel, on_delete=models.CASCADE, related_name='blog_rate')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog}-{self.rate}"


class LinkContainerModel(models.Model):
    blog = models.ForeignKey(
        CreateBlogModel, on_delete=models.CASCADE, related_name="blog_link")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class NotificationModel(TimeStampModel):
    fields = models.CharField(max_length=255, null=True, blank=True)
    viewed_status = models.BooleanField(default=False)
    blog = models.ForeignKey(
        CreateBlogModel, on_delete=models.CASCADE, null=True, blank=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE,
                              null=True, blank=True, related_name="other_user_notification")
    me_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(
        unique=False, max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.blog.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fields
