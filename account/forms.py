from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class userSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User
        fields = ['email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
    
# class CustomUserModel(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ('email','password')