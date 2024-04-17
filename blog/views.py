from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import FormView,TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.views import View
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.db.models import Q,Count,Avg,Exists,OuterRef,Max
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers import serialize   
from decouple import config
from django.dispatch import Signal
from django.http import Http404
import random
import re,json
import time

from blog.models import CreateBlogModel,BlogCommentModel,LikeModel,Rating,User,LinkContainerModel,NotificationModel
from blog.forms import CreateBlogForm,CommentForm
from account.views import userLogin
from account.models import Profile,Follow



class Home(ListView):
    template_name = 'home.html'
    model = CreateBlogModel

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status = 'public').order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = random.sample(list(CreateBlogModel.tags.all()),k = len(CreateBlogModel.tags.all()) if len(CreateBlogModel.tags.all()) < 5 else len(CreateBlogModel.tags.all()[:9]))

        blogs_with_likes = CreateBlogModel.objects.annotate(num_likes=Count('blog_like')).filter(num_likes__gt=0).order_by('-num_likes')[:5]
        context['most_likes'] = blogs_with_likes

        top_rated = Rating.objects.annotate(avg=Max('rate')).order_by('-avg')
        context['top_rated'] = top_rated

        link_container = LinkContainerModel.objects.filter(user = self.request.user) if self.request.user.is_authenticated else None
        context['link_container'] = link_container
        return context

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        blog_model = CreateBlogModel.objects.filter(Q(title__icontains=search_query) | Q(tags__name__icontains=search_query)).distinct()
        context = {
            'query':search_query,
            'searched':blog_model,
            'top_rated':Rating.objects.annotate(avg=Max('rate')).order_by('-avg'),
            'most_likes':CreateBlogModel.objects.annotate(num_likes=Count('blog_like')).filter(num_likes__gt=0).order_by('-num_likes')[:5],
            'link_container':LinkContainerModel.objects.filter(user = request.user) if request.user.is_authenticated else None
            # 'tag_search':CreateBlogModel.objects.filter(tags = Tag.objects.get(name = search_query)),
        }
        if search_query:
            return render(request,'home.html',context)
        else:
            return render(request,'home.html')
        # return render(request,'home.html',context)
    # return render(request,'home.html')


@method_decorator(login_required,name="dispatch")
class CreateBlog(View):

    def get(self,request):
        form = CreateBlogForm(request.POST or None)
        context = {'form':form}
        return render(request,'create_blog.html',context)

    def post(self,request):
        form = CreateBlogForm(request.POST or None)
        user_name = User.objects.get(email = self.request.user)
        if user_name.first_name == '' and user_name.last_name == '':
            return redirect(reverse('account:UpdateProfile',args=(self.request.user.profiles.id,)))
        else:
            if form.is_valid():
                print('valid')
                profan = config('profanity')
                profan_list = profan.split('-')
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']

                pattern = re.compile('<.*?>')
                result = re.sub(pattern,'',content)
                title_check = set(title.split(' ')).intersection(set(profan_list))
                if len(title_check) > 0 and len(result) > 0:
                    return HttpResponse('invalid content')
                else:
                    obj = form.save(commit = False)
                    obj.user = self.request.user
                    tags = self.request.POST.get('tags').split(',')
                    obj.save()
                    print(obj)
                    obj.tags.add(*tags)
                    if obj:
                        print('saved')
                        messages.info(self.request,'blog created successfully')
                        users,blog = self.request.user,obj.title
                        lst = [i.youser for i in Follow.objects.filter(follow = self.request.user)]
                        ope = list(map(lambda x:NotificationModel(fields=f"{users} posted a blog on {blog}",blog=obj,users=self.request.user,me_user=x).save(),lst))
                        return redirect(reverse('account:ProfileView',args=(self.request.user.id,)))
            return render(request,'create_blog.html')



@method_decorator(login_required,name='dispatch')
class UpdateBlog(UpdateView):
    model = CreateBlogModel
    template_name = 'create_blog.html'
    form_class = CreateBlogForm

    def form_valid(self, form):
        self.object = form.save()
        users,blog = self.request.user,self.object.title
        lst = [i.youser for i in Follow.objects.filter(follow=self.request.user)]
        list(map(lambda x:NotificationModel(fields=f"{users} updated a blog on {blog}",blog=self.object,users=self.request.user,me_user=x).save(),lst))
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

def BlogDetail(request,pk):
    blog_model = get_object_or_404(CreateBlogModel,status = 'public',id = pk)
    blog_model_tags = blog_model.tags.all()
    blog_comment_form = CommentForm(request.POST or None, request.FILES or None)
    profan = config('profanity')
    profan_list = profan.split('-')

    #parent comment
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
                    NotificationModel(fields=f"{obj.user} commented on your blog on {blog_model.title}",blog=blog_model,users=request.user,me_user=blog_model.user).save()
                    return redirect(reverse('blog:blog_detail', args=(blog_model.id,)))
                else:
                    request.session['next'] = pk
                    return redirect('account:userLogin')

    #child comment
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
            NotificationModel(fields=f"{request.user} commented on your blog on {blog_model.title}",blog=blog_model,users=request.user,me_user=blog_model.user).save()


    try:
        total_rate=sum([i.rate for i in Rating.objects.filter(blog__id = pk)])
        avg_rate=round(sum([i.rate for i in Rating.objects.filter(blog__id = blog_model.id)])/len(Rating.objects.filter(blog__id=blog_model.id)))
    except:
        avg_rate=0
        total_rate = 0


    saved_blog = None
    try:
        if request.user.is_authenticated:
            saved_blog = LinkContainerModel.objects.get(blog = CreateBlogModel.objects.get(id = pk),user = request.user)
        else:
            saved_blog = None
    except LinkContainerModel.DoesNotExist:
        pass
    context = {
        'blog_model':blog_model,
        'blog_model_tags':blog_model_tags,
        'blog_comment_form':blog_comment_form,
        'blog_comments':BlogCommentModel.objects.filter(blog_id = pk),
        'total_likes':len(LikeModel.objects.filter(blog = blog_model)),
        'total_rate':total_rate,
        'avg_rate':avg_rate,
        'saved_blog':saved_blog,
        'total_rate_user':len(Rating.objects.filter(blog__id=blog_model.id)),
        'like':LikeModel.objects.filter(blog=blog_model,user=request.user).exists() if request.user.is_authenticated else None,
        'profile_info':Profile.objects.get(user=blog_model.user),
        }
    return render(request,'read_blog.html',context)
    

# better_like 
@login_required
def like_post(request,pk):
    blog = get_object_or_404(CreateBlogModel,id = pk)
    like,created = LikeModel.objects.get_or_create(blog = blog,user = request.user)
    users,blog_title = request.user,blog.title
    NotificationModel(fields = f"{users} liked on your blog on {blog_title}",blog=blog,users=users,me_user = blog.user).save()
    if not created:
        if like:
            like.delete()
        else:
            return redirect(reverse('blog:blog_detail',args=(blog.id,)))
    return JsonResponse({'status':created,'total':len(LikeModel.objects.filter(blog = blog))},safe=False)



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
            blog,user = CreateBlogModel.objects.get(id = pk),request.user
            NotificationModel(fields=f"{user} rated on your blog on {blog.title}",blog=blog,users=request.user,me_user=blog.user).save()
            print("new object saved")
        else:
            rate_instance = Rating.objects.get(blog=CreateBlogModel.objects.get(id = pk),user=request.user)
            rate_instance.rate = rate_value
            rate_instance.save()
            print('updated')
    # return JsonResponse({'rate_instance':round(sum([i.rate for i in CreateBlogModel.objects.get(id = pk).blog_rate.all()])/len(CreateBlogModel.objects.get(id = pk).blog_rate.all()))},safe=False)
    return JsonResponse({'rate_instance':round(sum([i.rate for i in Rating.objects.filter(blog__id = pk)])/len(Rating.objects.filter(blog__id = pk)))
,'total_rate_fetch':sum([i.rate for i in Rating.objects.filter(blog__id = pk)]),'total_rate_user_fetch':len(Rating.objects.filter(blog=CreateBlogModel.objects.get(id = pk)))},safe=False)

def LinkContainer(request,pk):
    get,create = LinkContainerModel.objects.get_or_create(blog=CreateBlogModel.objects.get(id = pk),user = request.user)

    if not create:
        if get:
            get.delete()
            print('deleted')
        else:
            return redirect('blog:home')
    return JsonResponse({'status':'okay'},safe=False)
    

class NotificationView(View):
    def get(self,request):
        notification = NotificationModel.objects.filter(me_user = self.request.user) if self.request.user.is_authenticated else None
        try:
            serialize_notification = serialize('json',notification)
        except:
            serialize_notification = None
        return JsonResponse(serialize_notification,safe=False)
    
    def post(self,request):
        notification_id = json.loads(request.body)
        noti = notification_id.get('status')
        notification_model = get_object_or_404(NotificationModel,id = noti)
        notification_model.viewed_status = True
        notification_model.save()
        return JsonResponse({'status':'done'})


class Aboutpage(TemplateView):
    template_name = 'aboutus.html'


class Contactpage(TemplateView):
    template_name = 'contactus.html'
