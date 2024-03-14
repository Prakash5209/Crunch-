from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import get_user_model
from django.views.generic import FormView,TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decouple import config
from django.db.models import Q
import re,json

from blog.models import CreateBlogModel,BlogCommentModel,LikeModel,Rating
from account.models import User,Follow
from blog.forms import CreateBlogForm,CommentForm



class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        return CreateBlogModel.objects.filter(status = 'public')
    

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        print(search_query)
        blog_model = CreateBlogModel.objects.filter(Q(title__icontains=search_query))
        context = {'query':search_query,'searched':blog_model}
        return render(request,'home.html',context)

@method_decorator(login_required,name='dispatch')
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

        title_check = set(title.split(' ')).intersection(set(profan_list))
        print(title_check)
        # content_check = set(content.split(' ').intersection(set(profan_list)))
        if len(title_check) > 0 and len(result) > 0:
            return HttpResponse('invalid content')
        else:
            if obj.user == self.request.user:
                obj.save()
                print('content good')
                return super().form_valid(form)
            else:
                return render(self.request,'home.html')
        # obj.save()
    
    
def BlogDetail(request,pk):
    blog_model = get_object_or_404(CreateBlogModel,status = 'public',id = pk)
    blog_comment_form = CommentForm(request.POST or None, request.FILES or None)
    profan = config('profanity')
    profan_list = profan.split('-')

    if request.method == 'POST':
        if blog_comment_form.is_valid():

            raw_comment = blog_comment_form.cleaned_data['comment']

            pattern = re.compile('<.*?>')
            result = re.sub(pattern,'',raw_comment)
            title_check = set(raw_comment.split(' ')).intersection(set(profan_list))

            if len(title_check) > 0 and len(result) > 0:
                return HttpResponse('invalid content')
            else:
                    
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
        raw_reply = request.POST.get('reply')
        pattern = re.compile('<.*?>')
        result = re.sub(pattern,'',raw_reply)
        title_check = set(raw_reply.split(' ')).intersection(set(profan_list))

        if len(title_check) > 0 and len(result) > 0:
            return HttpResponse('invalid content')
        else:
            BlogCommentModel(user=request.user,blog_id=blog_model,parent_comment=BlogCommentModel.objects.get(id = int(comment_id)),comment=comment).save() if request.user.is_authenticated else None        
        # print('saved')

    try:
        total_rate=round(sum([i.rate for i in Rating.objects.filter(blog=blog_model)])/len(Rating.objects.filter(blog=blog_model)))
    except:
        total_rate = 0

    context = {
        'blog_model':blog_model,
        'blog_comment_form':blog_comment_form,
        'blog_comments':BlogCommentModel.objects.filter(blog_id = pk),
        'total_likes':len(LikeModel.objects.all()),
        'total_rate':total_rate,
        'total_rate_user':len(Rating.objects.filter(blog__id=blog_model.id)),
        'like':LikeModel.objects.filter(blog=blog_model,user=request.user).exists(),
        }
    return render(request,'read_blog.html',context)
    

# better_like 
@login_required
def like_post(request,pk):
    blog = get_object_or_404(CreateBlogModel,id = pk)
    like,created = LikeModel.objects.get_or_create(blog = blog,user = request.user)
    if not created:
        if like:
            like.delete()
        else:
            return redirect(reverse('blog:blog_detail',args=(blog.id,)))
    return JsonResponse({'status':created,'total':len(LikeModel.objects.all())},safe=False)



@method_decorator(login_required,name='dispatch')
class UpdateBlog(UpdateView):
    model = CreateBlogModel
    # fields = ['title','content']
    template_name = 'create_blog.html'
    form_class = CreateBlogForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        var =  self.request.POST.get('status')
        if var == 'public':
            messages.success(self.request,"blog updated!")
            return reverse_lazy('blog:blog_detail',kwargs={'pk':self.object.pk})
        else:
            messages.success(self.request,"blog updated!")
            return reverse_lazy('blog:home')
        # return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required,name='dispatch')
class DeleteBlog(DeleteView):
    model = CreateBlogModel
    success_url = reverse_lazy('blog:home')
    template_name = 'read_blog.html'

@login_required
def DeleteComment(request, pk):
    comment_model = get_object_or_404(BlogCommentModel,id = pk,user = request.user)
    comment_model.delete()
    return redirect(reverse('blog:blog_detail', kwargs={'pk': comment_model.blog_id.id}))


def rateBlog(request,pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        rate_value = data.get('rating_value')
        print('rate')
        var = Rating.objects.filter(Q(blog__id=pk) & Q(user=request.user)).exists()
        if not var:
            Rating(rate=rate_value,blog=CreateBlogModel.objects.get(id=pk),user=request.user).save()
            print("new object saved")
        else:
            rate_instance = Rating.objects.get(blog=CreateBlogModel.objects.get(id = pk),user=request.user)
            rate_instance.rate = rate_value
            rate_instance.save()
            print('updated')
    return JsonResponse({'status':'okay'},safe=False)


class Aboutpage(TemplateView):
    template_name = 'aboutus.html'


class Contactpage(TemplateView):
    template_name = 'contactus.html'


