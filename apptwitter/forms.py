from django import forms

from .models import Messages

class PostForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('id', 'text')
