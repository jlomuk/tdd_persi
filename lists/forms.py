from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ('text', )  
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg', 
            })
        }
        error_messages = {
            'text': {'required': 'You can not have an empty list item'}
        }

