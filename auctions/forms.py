from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.urls import reverse
from django import forms

from .models import List, Bid, WahchList, Comment

class AddList(forms.ModelForm):

    class Meta:
        model = List
        fields = ('title', 'category', 'start_bid','description','img_url',"user_id")
        widgets = {'user_id': forms.HiddenInput()}



class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('item_id', 'bid', "user_id")
        widgets = {'user_id': forms.HiddenInput(), 'item_id': forms.HiddenInput()}


class WahchListForm(forms.ModelForm):

    class Meta:
        model = WahchList
        fields = ('item_id', "user_id")
        widgets = {'user_id': forms.HiddenInput(), 'item_id': forms.HiddenInput()}

class TurnOff(forms.ModelForm):

    class Meta:
        model = List
        fields = ('active',)
        widgets = {'active': forms.HiddenInput(),}



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body', 'item_id', 'user_id')

        widgets = {'user_id': forms.HiddenInput(), 'item_id': forms.HiddenInput(), 'name':forms.HiddenInput()}

class CategoryForm(forms.ModelForm):
    
    class Meta:
            model = List

            fields = ('category',)

