from django import forms
from tinymce.widgets import TinyMCE

from blog.models import CreateBlogModel

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = CreateBlogModel
        exclude = ('user',)
        widgets = {
            # 'image':forms.ImageField(attrs={'class':'form-control'}),
            'content':TinyMCE(),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'title'}),
            'status':forms.Select(attrs={'class':'form-control'}),
        }
    
