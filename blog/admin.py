from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from blog.models import CreateBlogModel,BlogCommentModel


admin.site.register(BlogCommentModel)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }



admin.site.register(CreateBlogModel,YourModelAdmin)