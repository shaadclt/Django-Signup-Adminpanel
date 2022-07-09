from django import forms 
from django.contrib.auth.models import User

class UserUpdation(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
        
