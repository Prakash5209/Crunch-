from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,logout,login
from django.contrib import messages
from django.views import View
from django.urls import reverse


from account.models import User,Profile
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
        # Retrieve the Profile object based on the provided pk
        profile_model = get_object_or_404(Profile, user_id=pk)
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        form = ProfileForm(instance=profile_model,initial = initial_data)
        
        # Render the profile.html template with the form and profile_model
        context = {'profile_model': profile_model, 'form': form}
        return render(request, 'profile.html', context)

    def post(self, request, pk):
        # Retrieve the User object based on the provided pk
        user = get_object_or_404(User, id=pk)
        
        profile_model = get_object_or_404(Profile, user_id=pk)
        form = ProfileForm(request.POST, instance=profile_model)
        
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            form.save()
            print('Profile updated successfully')
            # Redirect to the ProfileView with the updated user's id
            return redirect(reverse('account:ProfileView', kwargs={'pk': pk}))
        
        # If form is not valid, render the profile.html template with the form and profile_model
        context = {'profile_model': profile_model, 'form': form}
        return render(request, 'profile.html', context)


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