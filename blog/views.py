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
import requests
import re

from account.models import User
from blog.models import CreateBlogModel,BlogCommentModel
from blog.forms import CreateBlogForm,CommentForm

from decouple import config


class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        return CreateBlogModel.objects.filter(status = 'public')


# class CreateBlog(FormView):
#     template_name = 'create_blog.html'
#     form_class = CreateBlogForm
#     success_url = "/"

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.user = self.request.user

#         # Obtain text from the form
#         text = form.cleaned_data['title']
#         print(text)

#         # Call the Perspective API to analyze toxicity
#         toxicity_score = self.analyze_toxicity('text')

#         # Here, you can use the toxicity_score to decide whether to save the object or not
#         if toxicity_score is not None and toxicity_score <= 0.7:
#             obj.save()
#             return super().form_valid(form)
#         else:
#             # Optionally, you can render a template indicating that the content is toxic
#             return render(self.request, 'toxic_content.html')
        
#     def analyze_toxicity(self, text):
#         api_key = 'AIzaSyATP0DR9mYqI45FF1JQrmAcwvZuBQoRI9U'  # Replace with your Perspective API key

#         # API endpoint for analyzing text toxicity
#         perspective_api_url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

#         # Parameters for the API request
#         params = {
#             'key': api_key,
#         }

#         # Request body containing the text to analyze
#         json_data = {
#             'comment': {'text': text},
#             'languages': ['en'],  # Assuming English language
#             'requestedAttributes': {'TOXICITY': {}},  # Request toxicity score
#         }

#         try:
#             # Make POST request to Perspective API
#             response = requests.post(perspective_api_url, params=params, json=json_data)

#             if response.status_code == 200:
#                 data = response.json()
#                 toxicity_score = data['attributeScores']['TOXICITY']['summaryScore']['value']
#                 print("Toxicity score:", toxicity_score)  # Debugging print
#                 return toxicity_score
#             else:
#                 # Handle API error
#                 print("API error:", response.status_code, response.reason)  # Debugging print
#                 return None
#         except Exception as e:
#             # Handle other exceptions
#             print("Exception during API call:", e)  # Debugging print
#             return None



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
            # obj.save()
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
        comment_id = request.POST.get('comment_id')
        comment = request.POST.get('reply')
        
        BlogCommentModel(user=request.user,blog_id=blog_model,parent_comment=BlogCommentModel.objects.get(id = int(comment_id)),comment=comment).save() if request.user.is_authenticated else None
        print('saved')

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


# def DeleteBlog(request,pk):
#     CreateBlogModel.objects.get(id = pk).delete()
#     return redirect(reverse('blog:home'))
    
class DeleteBlog(DeleteView):
    model = CreateBlogModel
    success_url = reverse_lazy('blog:home')
    template_name = 'read_blog.html'

class Aboutpage(TemplateView):
    template_name = 'aboutus.html'


class Contactpage(TemplateView):
    template_name = 'contactus.html'


    # AIzaSyATP0DR9mYqI45FF1JQrmAcwvZuBQoRI9U