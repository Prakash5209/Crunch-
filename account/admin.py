from django.contrib import admin

from account.models import User,Follow

admin.site.register(User)
admin.site.register(Follow)