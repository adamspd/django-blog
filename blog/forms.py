from django import forms
from blog.models import Tag, BlogPost as Post, Category, BlogEntry

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