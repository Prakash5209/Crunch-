from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,get_user_model,logout,login
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from account.models import User
from account.forms import userSignupForm

activeUser = get_user_model()

def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request,email = email,password = password)
        if user:
            login(request,user)
            return redirect('blog:home')
        else:
            messages.info(request, "incorrect input")
    return render(request,'login.html')


# def userSignup(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 == password2 and len(password2) > 8:
#             User(email = email,password = make_password(password2)).save()
#             return redirect('account:userLogin')
#             print('registered')
#     return render(request,'signup.html')

def userSignup(request):
    form = userSignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('blog:home')
    print(request.POST.get('email'))
    return render(request,'signup.html',context={'form':form})


def userLogout(request):
    logout(request)
    return redirect('blog:home')