from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User,Profile

class userSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User    
        fields = ['email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for i in self.fields:
            self.fields[i].widget.attrs.update({'class':'form-control'})
    

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = ['avatar','first_name','last_name','address','dob','gender','bio']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for i in self.fields:
            if i == 'dob':
                self.fields[i].widget.attrs.update({'placeholder':'yyyy-mm-dd'})
            self.fields[i].widget.attrs.update({'class':'form-control'})
