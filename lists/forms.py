from django import forms
from django.core.exceptions import ValidationError

from .models import Item, List


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': 'You can not have an empty list item'}
        }

    def save(self, for_list, *args, **kwargs):
        self.instance.list = for_list
        return super().save(*args, **kwargs)


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'],
                            owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': ['You have already got this in your list']}
            self._update_errors(e)

    def save(self, *args, **kwargs):
        return super(forms.ModelForm, self).save(*args, **kwargs)
