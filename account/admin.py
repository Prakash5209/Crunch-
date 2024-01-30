from django.contrib import admin

from account.models import User
from blog.models import CreateBlogModel

admin.site.register(User)
admin.site.register(CreateBlogModel)