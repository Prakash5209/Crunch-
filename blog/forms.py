from django import forms
from tinymce.widgets import TinyMCE

from blog.models import CreateBlogModel

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = CreateBlogModel
        exclude = ('user',)
        widgets = {
            'content':TinyMCE(),
            'title':forms.TextInput(attrs={'class':'form-control'})
        }