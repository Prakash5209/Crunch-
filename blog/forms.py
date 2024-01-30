from django import forms

from blog.models import CreateBlogModel

class CreateBlogForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'id':'richtext_field'}))
    class Meta:
        model = CreateBlogModel
        exclude = ('user',)