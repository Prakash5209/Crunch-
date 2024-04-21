from django import forms
from tinymce.widgets import TinyMCE

from blog.models import CreateBlogModel,BlogCommentModel

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = CreateBlogModel
        exclude = ('user','slug')
        widgets = {
            # 'image':forms.ImageField(attrs={'class':'form-control'}),
            'content':TinyMCE(),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'title'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            # 'tags':forms.TextInput(attrs={'class':'form-control','placeholder':'tags'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ('comment',)
        widgets = {
            'comment':forms.TextInput(attrs={'class':'form-control','placeholder':'write a comment'})
        }
    
