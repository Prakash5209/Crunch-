from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

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

class BlogDetail(DetailView):
    model = CreateBlogModel
    template_name = 'read_blog.html'
    context_object_name = 'object'


class UpdateBlog(UpdateView):
    model = CreateBlogModel
    # fields = ['title','content']
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = '/'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if the post is a new one
        context['is_new_post'] = not self.object.pk
        
        return context

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})
    

# class DeleteBlog(DeleteView):
#     queryset = CreateBlogModel.objects.all()
#     success_url = reverse_lazy('blog:home')



