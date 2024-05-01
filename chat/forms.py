from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,ButtonHolder,Submit

from chat.models import ChatModel

class ChatModelForm(forms.ModelForm):
    class Meta:
        model = ChatModel
        fields = ('text',)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['text'].required = False
        self.fields['text'].label = ''
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('text',rows=2,css_class='form-control',placeholder='message',label = False),
            ButtonHolder(
                Submit('submit','Send',css_class='btn-primary btn-sm')
            )
        )
