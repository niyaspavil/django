from django import forms
from rango.models import Category, Page


class CategoryForms(forms.ModelForm):

    name  = forms.CharField(max_length = 128, help = "Please enter category name")
    views = forms.IntegerField(widjet=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)


    class meta:
	model = Category


class PageForms(forms.ModelForms):

    title = forms.Charfield(max_length=128, help= "Please enter title of the page")
    url   = forms.URLField(max_length=200, help = "Please enter url of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)


    class meta:
	model = Page

        fields = ('title', 'url', 'views')


