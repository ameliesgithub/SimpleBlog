from django.forms import forms, ModelForm
from django.forms.widgets import TextInput, Textarea, Select, FileInput

from blog.models import Post


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'snippet', 'header_image', 'author']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'snippet': TextInput(attrs={'class': 'form-control'}),
            'header_image': FileInput(attrs={'class': 'form-control'}),
            'author': Select(attrs={'class': 'form-control'}),
        }

class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'snippet', 'header_image']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'snippet': TextInput(attrs={'class': 'form-control'}),
            'header_image': FileInput(attrs={'class': 'form-control'}),
        }