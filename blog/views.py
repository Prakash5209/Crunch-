from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView

from account.models import User
from blog.models import CreateBlogModel,BlogCommentModel
from blog.forms import CreateBlogForm,CommentForm

class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel
    
    def get_queryset(self):
        return CreateBlogModel.objects.filter(status = 'public')

class CreateBlog(FormView):
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = "/"

    def form_valid(self,form):
        obj = form.save(commit = False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
    
def BlogDetail(request,pk):
    blog_model = CreateBlogModel.objects.get(id = pk)

    print(blog_model)
    blog_comment_form = CommentForm(request.POST or None)

    if blog_comment_form.is_valid():
        obj = blog_comment_form.save(commit=False)
        obj.user = request.user
        obj.blog_id = blog_model
        obj.save()
        return redirect(reverse('blog:blog_detail', args=(blog_model.id,)))
        # return render(reverse('blog:blog_detail',args = (blog_model.id,)))
    blog_comment_model = BlogCommentModel.objects.filter(blog_id = pk)
    print(blog_comment_model)

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
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if the post is a new one
        context['is_new_post'] = not self.object.pk
        
        return context

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class DeleteBlog(DeleteView):
    queryset = CreateBlogModel.objects.all()
    success_url = reverse_lazy('blog:home')



