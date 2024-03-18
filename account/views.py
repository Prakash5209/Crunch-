from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,logout,login
from django.views.generic import UpdateView
from django.contrib import messages
from django.views import View
from django.urls import reverse,reverse_lazy
from django.db.models import Q


from account.models import User,Profile,Follow
from blog.models import CreateBlogModel
from account.forms import userSignupForm,ProfileForm

activeUser = get_user_model()

def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email = email,password = password)
        if user:
            login(request,user)
            return redirect('blog:home')
        else:
            messages.info(request, "incorrect input")
    return render(request,'login.html')


class ViewProfile(View):

    def get(self, request, pk):
        profile_model = get_object_or_404(Profile, user_id=pk)
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileForm(instance=profile_model,initial = initial_data)

        following = Follow.objects.filter(youser = pk)
        follower = Follow.objects.filter(follow = pk)

        context = {
            'profile_model': profile_model,
            'form': form,
            'CreateBlogModel':CreateBlogModel.objects.filter(user = self.request.user),
            'following':following,
            'follower':follower,
            }
        return render(request, 'profile.html', context)

    # def post(self, request, pk):
    #     user = get_object_or_404(User, id=pk)
    #     profile_model = get_object_or_404(Profile, user_id=pk,user = request.user)
    #     form = ProfileForm(request.POST,request.FILES or None, instance=profile_model)
    #     if form.is_valid():
    #         user = request.user
    #         user.first_name = form.cleaned_data.get('first_name')
    #         user.last_name = form.cleaned_data.get('last_name')
    #         user.save()
    #         form.save()
    #         print('Profile updated successfully')
    #         return redirect(reverse('account:ProfileView', kwargs={'pk': pk}))

    #     context = {'profile_model': profile_model, 'form': form}
    #     return render(request, 'profile.html', context)

class UpdateProfile(UpdateView):
    model = Profile
    form_class=ProfileForm
    template_name = 'update_profile.html'
    # success_url = reverse_lazy('account:ProfileView',kwargs={'pk':object.pk})
    
    def get_initial(self) -> dict[str, Any]:
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
        if Follow.objects.filter(youser=self.request.user,follow=int(pk)).exists():
            Follow.objects.filter(youser=self.request.user,follow=int(pk)).delete()
            print('success unfollowed')
            return redirect(reverse('account:ProfileView',args=(pk,)))
        else:
            Follow(youser=self.request.user,follow=User.objects.get(id=int(pk))).save()
            print('success follow')
            return redirect(reverse('account:ProfileView',args=(pk,)))
        return render(request,'profile.html')


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
    return redirect('blog:home')


class Library(View):
    def get(self,request):
        blog_public = CreateBlogModel.objects.filter(user = request.user)
        context = {
            'blog_public':blog_public,
        }
        return render(request,'library.html',context)
