from django import forms
from blog.models import Tag, BlogPost as Post

choices = Tag.objects.all().values_list('name', 'name')

choice_list = []
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'header_img', 'author', 'headline', 'content', 'tag')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'header_img': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tag': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'header_img', 'headline', 'content', 'tag')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'header_img': forms.TextInput(attrs={'class': 'form-control'}),
            'headline': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tag': forms.Textarea(attrs={'class': 'form-control'}),
        }
