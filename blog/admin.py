from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from blog.models import CreateBlogModel,BlogCommentModel,LikeModel,Rating,LinkContainerModel,NotificationModel
from account.models import Profile


admin.site.register(BlogCommentModel)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }



admin.site.register(CreateBlogModel,YourModelAdmin)
admin.site.register(LikeModel)
admin.site.register(Rating)
admin.site.register(LinkContainerModel)
admin.site.register(NotificationModel)
