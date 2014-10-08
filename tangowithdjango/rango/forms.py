from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User


class CategoryForms(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name', 'views', 'likes')


class PageForms(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter title of the page")
    url = forms.URLField(max_length=200, help_text="Please enter url of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page

        fields = ('title', 'url', 'views')


    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
class UserForm (forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username")
    email = forms.EmailField(help_text="please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter your password")

    class Meta:
        model =User
        fields = ('username','email','password')

class UserProfileForm (forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload", required=False)
    class Meta:
        model = UserProfile
        fields = ['website','picture']



