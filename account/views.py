from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,logout,login
from django.views.generic import UpdateView
from django.contrib import messages
from django.views import View
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView,DeleteView
from django.db.models import Exists,Count,Subquery,OuterRef,Q
from taggit.models import Tag
from django.contrib.auth.models import User

from account.models import User,Profile,Follow
from blog.models import CreateBlogModel,Rating,BlogCommentModel,LinkContainerModel
from account.forms import userSignupForm,ProfileForm

activeUser = get_user_model()

def userLogin(request,**kwargs):
    print(kwargs.get('data'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email = email,password = password)
        if user:
            login(request,user)
            var = User.objects.get(email = request.user)
            if(var.first_name == '' and var.last_name == ''):
                messages.info(request,"you cannot post any blog without filling your details")
                try:
                    return redirect(reverse('account:UpdateProfile',args=(request.user.profiles.id,)))
                except:
                    return redirect('blog:home')
            else:
                messages.info(request,'logged in successfully')
                print('session',request.session.get('next'))
                if request.session.get('next'):
                    return redirect(reverse('blog:blog_detail',args=(request.session.get('next'),)))
                if request.session.get('next'):
                    del(request.session['next'])
                return redirect('blog:home')
        else:
            messages.info(request, "incorrect input")
    return render(request,'login.html')


class ViewProfile(View):

    def get(self, request, pk):
        profile_model = get_object_or_404(Profile, user_id=pk)
        user = User.objects.get(id = pk)
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileForm(instance=profile_model,initial = initial_data)

        following =[i.follow for i in Follow.objects.filter(youser = User.objects.get(id = pk))]
        follower =[i.youser for i in Follow.objects.all() if i.follow == User.objects.get(id = pk)]
        following_bool = True if self.request.user in follower else False
        total_likes = sum([len(i.blog_like.all()) for i in CreateBlogModel.objects.filter(user__id = pk)])
        total_contents = CreateBlogModel.objects.filter(user__id = pk)
        my_blog = CreateBlogModel.objects.filter(user__id = pk,status = 'public')
        total_rating = 0
        for i in my_blog:
            total_rating = total_rating + sum([j.rate for j in Rating.objects.filter(blog = i)])

        total_comments = BlogCommentModel.objects.filter(user = user).count()

        context = {
            'profile_model': profile_model,
            'form': form,
            'CreateBlogModel':CreateBlogModel.objects.filter(user__id = pk,status = 'public'),
            'following':following,
            'follower':follower,
            'total_likes':total_likes,
            'total_contents':total_contents,
            'total_rating':total_rating,
            'total_comments':total_comments,
            'following_bool':following_bool,
            }
        return render(request, 'profile.html', context)


class UpdateProfile(UpdateView):
    model = Profile
    form_class=ProfileForm
    template_name = 'update_profile.html'
    # success_url = reverse_lazy('account:ProfileView',kwargs={'pk':object.pk})
    
    def get_initial(self):
        initial_data =  super().get_initial()
        initial_data = {
            'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name,
        }
        return initial_data
    
    def get_success_url(self):
        return reverse('account:ProfileView',args=(self.object.user.pk,))
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        messages.success(self.request, "Profile details updated.")
        return super().form_valid(form)

class FollowInProfile(View):
    def get(self,request,pk):
        get,create = Follow.objects.get_or_create(youser = self.request.user,follow = User.objects.get(id = pk))
        if not create:
            if get:
                get.delete()
            else:
                return redirect(reverse('account:ProfileView',args=(pk,)))

        return redirect(reverse('account:ProfileView',args=(pk,)))           


def userSignup(request):
    form = userSignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user = user)
        return redirect('account:userLogin')
    print(request.POST.get('email'))
    return render(request,'signup.html',context={'form':form})


def userLogout(request):
    logout(request)
    messages.info(request,'logged out successfully')
    return redirect('blog:home')


class Library(View):
    def get(self,request):
        user_blog = CreateBlogModel.objects.filter(user = request.user)
        
        saved_blog = CreateBlogModel.objects.annotate(has_link = Exists(LinkContainerModel.objects.filter(blog__id = OuterRef('pk'),user = request.user))).filter(has_link = True)
        
        context = {
            'user_blog':user_blog,
            'saved_blog':saved_blog,
        }
        return render(request,'library.html',context)



def search_feature_library(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        blog_model = CreateBlogModel.objects.filter(user = request.user,title__icontains=search_query,tags__name__icontains=search_query)
        print(blog_model)
        context = {
            'query':search_query,
            'searched':blog_model,
            # 'tag_search':CreateBlogModel.objects.filter(tags = Tag.objects.get(name = search_query)),
        }
        return render(request,'library.html',context)
    return render(request,'library.html')


@method_decorator(login_required,name='dispatch')
class DeleteBlog_library(DeleteView):
    model = CreateBlogModel
    success_url = reverse_lazy('account:Library')
    template_name = 'read_blog.html'


class Forgot_password(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        verify_email = None
        try:
            verify_email = User.objects.get(email = email)
        except:
            verify_email = None

        if verify_email != None and password == confirm_password:
            verify_email.set_password(confirm_password)
            verify_email.save()
            print('saved')
            return redirect('account:userLogin')
            
        return render(request,'fpassword.html')

    def get(self, request):
        return render(request,'fpassword.html')
