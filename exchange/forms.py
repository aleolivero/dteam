from django import forms
from django.forms import ModelForm
from exchange.models import Chat
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ChatForm(forms.ModelForm): 
    
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta: 
        model = Chat 
        fields = ['content']

