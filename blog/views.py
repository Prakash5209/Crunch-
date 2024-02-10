from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from django.views.generic import FormView,TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
import re

from account.models import User
from blog.models import CreateBlogModel,BlogCommentModel
from account.models import User
from blog.forms import CreateBlogForm,CommentForm

from decouple import config


class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        return CreateBlogModel.objects.filter(status = 'public')

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        print(search_query)
        blog_model = CreateBlogModel.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        context = {'query':search_query,'searched':blog_model}
        return render(request,'home.html',context)
        
class CreateBlog(FormView):
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = "/"

    def form_valid(self,form):
        obj = form.save(commit = False)
        obj.user = self.request.user

        profan = config('profanity')
        profan_list = profan.split('-')
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        pattern = re.compile('<.*?>')
        result = re.sub(pattern,'',content)
        print(result)

        title_check = set(title.split(' ')).intersection(set(profan_list))
        # content_check = set(content.split(' ').intersection(set(profan_list)))
        if len(title_check) > 0 and len(result) > 0:
            return HttpResponse('invalid content')
        else:
            obj.save()
            print('content good')
            return super().form_valid(form)
        # obj.save()
    
    
def BlogDetail(request,pk):
    blog_model = get_object_or_404(CreateBlogModel,status = 'public',id = pk)

    blog_comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if blog_comment_form.is_valid():
            obj = blog_comment_form.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user 
                obj.blog_id = blog_model
                obj.save()
                return redirect(reverse('blog:blog_detail', args=(blog_model.id,)))
            else:
                return redirect('account:userLogin')
        
    if request.method == 'POST':
        comment_id = request.POST.get('parent_comment_id')
        comment = request.POST.get('reply')
        print(comment_id,comment)
        
        BlogCommentModel(user=request.user,blog_id=blog_model,parent_comment=BlogCommentModel.objects.get(id = int(comment_id)),comment=comment).save() if request.user.is_authenticated else None
        # print('saved')

        # return render(reverse('blog:blog_detail',args = (blog_model.id,)))
    blog_comment_model = BlogCommentModel.objects.filter(blog_id = pk)

    context = {'blog_model':blog_model,'blog_comment_form':blog_comment_form,'blog_comments':blog_comment_model}
    return render(request,'read_blog.html',context)
    

class UpdateBlog(UpdateView):
    model = CreateBlogModel
    # fields = ['title','content']
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = '/'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Check if the post is a new one
    #     context['is_new_post'] = not self.object.pk
        
    #     return context

    def get_success_url(self):
        messages.success(self.request,"blog updated!")
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

    
class DeleteBlog(DeleteView):
    model = CreateBlogModel
    success_url = reverse_lazy('blog:home')
    template_name = 'read_blog.html'

class Aboutpage(TemplateView):
    template_name = 'aboutus.html'


class Contactpage(TemplateView):
    template_name = 'contactus.html'


    # AIzaSyATP0DR9mYqI45FF1JQrmAcwvZuBQoRI9U