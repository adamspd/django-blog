"""
@author: Adams Pierre David
@contact: https://adamspierredavid.com/contact
@website: https://adamspierredavid.com
@license: MIT
@version: 1.0.0
@created: 2022-08-01
@updated: 2022-10-07
@description: blog application forms.
"""

from django import forms

from blog.models import Tag, BlogPost as Post, Category, BlogEntry, BreakingNews

choices = Tag.objects.all().values_list('name', 'name')

choice_list = []
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'header_img', 'author', 'headline', 'table_content', 'content', 'tag')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'header_img': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.Textarea(attrs={'class': 'form-control'}),
            'table_content': forms.Textarea(attrs={'class': 'form-control'}),
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


class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PublishedPostForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ('status', 'category')

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class AddBreakingNewsForm(forms.ModelForm):
    class Meta:
        model = BreakingNews
        fields = ('title', 'content', 'is_active')

        widgets = {
            'breaking_news': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    hidden = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {
                'type': 'text',
                'class': 'form-control',
                'onkeyup': 'return forceTitle(this);',
                'placeholder': 'Your name',
            })
        self.fields['email'].widget.attrs.update(
            {
                'type': 'email',
                'class': 'form-control',
                'onkeyup': 'return forceLower(this);',
                'placeholder': 'Your email',
            })
        self.fields['hidden'].widget.attrs.update(
            {
                'type': 'hidden',
                'class': 'hidden-value',
                'placeholder': 'Subject',
            })
