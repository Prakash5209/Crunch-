from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView,TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decouple import config
from django.http import Http404
import random
import re,json

from blog.models import CreateBlogModel,BlogCommentModel,LikeModel,Rating,User
from blog.forms import CreateBlogForm,CommentForm

from taggit.models import Tag

class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        print(self.request.user)
        queryset = super().get_queryset()
        queryset = queryset.filter(status = 'public')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = random.sample(list(CreateBlogModel.tags.all()),k = len(CreateBlogModel.tags.all()))
        return context

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        blog_model = CreateBlogModel.objects.filter(Q(title__icontains=search_query) | Q(tags__name__icontains=search_query)).distinct()
        context = {
            'query':search_query,
            'searched':blog_model
            # 'tag_search':CreateBlogModel.objects.filter(tags = Tag.objects.get(name = search_query)),
        }
        return render(request,'home.html',context)
    return render(request,'home.html')


@method_decorator(login_required,name='dispatch')
class CreateBlog(FormView):
    template_name = 'create_blog.html'
    form_class = CreateBlogForm
    success_url = "/"

    def form_valid(self,form):
        profan = config('profanity')
        profan_list = profan.split('-')
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']

        pattern = re.compile('<.*?>')
        result = re.sub(pattern,'',content)

        title_check = set(title.split(' ')).intersection(set(profan_list))
        # content_check = set(content.split(' ').intersection(set(profan_list)))
        if len(title_check) > 0 and len(result) > 0:
            return HttpResponse('invalid content')
        else:
            user_name = User.objects.get(email = self.request.user)
            if user_name.first_name == '' and user_name.last_name == '':
                return redirect(reverse('account:UpdateProfile',args=(self.request.user.profiles.id,)))
            else:
                obj = form.save(commit = False)
                obj.user = self.request.user
                obj.save()
                tags = self.request.POST.get('tags').split(',')
                obj.tags.add(*tags)
                if obj.save():
                    return redirect(reverse('account:ProfileView',args=(self.request.user.profiles.id,)))
                print('valid content')
                return super().form_valid(form)
            return redirect('blog:home')
            # return redirect(reverse('account:UpdateProfile',args=(self.request.user.profiles,)))
        # else:
        #     var = User.objects.get(email = self.request.user)
        #     if var.first_name and var.last_name == '':
        #         return redirect(reverse('account:UpdateProfile',args=(self.request.user.profiles,)))
        #     else:
        #         obj = form.save(commit = False)
        #         obj.user = self.request.user
        #         obj.save()
        #         tags = self.request.POST.get('tags').split(',')
        #         obj.tags.add(*tags)
        #         if obj.save():
        #             return redirect(reverse('account:ProfileView',args=(self.request.user.profiles,)))
        #         print('content good')
        #         return super().form_valid(form)
        #     return render(self.request,'home.html')
    
    
def BlogDetail(request,pk):
    blog_model = get_object_or_404(CreateBlogModel,status = 'public',id = pk)
    blog_model_tags = blog_model.tags.all()
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
        total_rate=sum([i.rate for i in Rating.objects.filter(blog__id = pk)])
    except:
        total_rate = 0

    try:
        avg_rate=len(Rating.objects.filter(blog__id=blog_model.id))
    except:
        avg_rate=0

    context = {
        'blog_model':blog_model,
        'blog_model_tags':blog_model_tags,
        'blog_comment_form':blog_comment_form,
        'blog_comments':BlogCommentModel.objects.filter(blog_id = pk),
        'total_likes':len(LikeModel.objects.filter(blog = blog_model)),
        'total_rate':total_rate,
        'avg_rate':avg_rate,
        'total_rate_user':len(Rating.objects.filter(blog__id=blog_model.id)),
        'like':LikeModel.objects.filter(blog=blog_model,user=request.user).exists() if request.user.is_authenticated else None,
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
    return JsonResponse({'status':created,'total':len(LikeModel.objects.filter(blog = blog))},safe=False)



@method_decorator(login_required,name='dispatch')
class UpdateBlog(UpdateView):
    model = CreateBlogModel
    template_name = 'create_blog.html'
    form_class = CreateBlogForm

    def form_valid(self, form):
        print(self.object)
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
    
    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.user != self.request.user:
            raise Http404("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

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
        print(rate_value)
        var = Rating.objects.filter(Q(blog__id=pk) & Q(user=request.user)).exists()
        if not var:
            Rating(rate=rate_value,blog=CreateBlogModel.objects.get(id=pk),user=request.user).save()
            print("new object saved")
        else:
            rate_instance = Rating.objects.get(blog=CreateBlogModel.objects.get(id = pk),user=request.user)
            rate_instance.rate = rate_value
            rate_instance.save()
            print('updated')
    # return JsonResponse({'rate_instance':round(sum([i.rate for i in CreateBlogModel.objects.get(id = pk).blog_rate.all()])/len(CreateBlogModel.objects.get(id = pk).blog_rate.all()))},safe=False)
    return JsonResponse({'rate_instance':round(sum([i.rate for i in Rating.objects.filter(blog__id = pk)])/len(Rating.objects.filter(blog__id = pk)))
,'total_rate_fetch':sum([i.rate for i in Rating.objects.filter(blog__id = pk)]),'total_rate_user_fetch':len(Rating.objects.filter(blog=CreateBlogModel.objects.get(id = pk)))},safe=False)


class Aboutpage(TemplateView):
    template_name = 'aboutus.html'


class Contactpage(TemplateView):
    template_name = 'contactus.html'