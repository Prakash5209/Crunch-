from django.contrib import admin

from account.models import User,Follow,Profile

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Profile)