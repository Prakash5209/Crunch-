from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.views.generic import FormView
from django.views.generic.list import ListView

from account.models import User
from blog.models import CreateBlogModel
from blog.forms import CreateBlogForm

class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        return CreateBlogModel.objects.all()

class CreateBlog(FormView):
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = "/"

    def form_valid(self,form):
        obj = form.save(commit = False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)