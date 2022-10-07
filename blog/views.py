from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

from blog.forms import AddTagForm, AddCategoryForm
from blog.models import BlogPost as Post, Tag, PUBLISHED, BlogEntry, Category, BreakingNews
from blog.utils import generate_rgba_color


def get_context_data(request):
    if request.user.is_authenticated:
        post_user_logged = BlogEntry.objects.all().order_by('-pub_date')
        return post_user_logged
    else:
        post = BlogEntry.objects.all().filter(status=PUBLISHED).order_by('-pub_date')
        return post


# Write a function to paginate posts
def paginate_posts(request, posts, num):
    # Paginate posts
    paginator = Paginator(posts, num)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts


def view_all_article(request):
    posts = get_context_data(request=request)
    cat_list = Category.objects.all()
    tag_list = Tag.objects.all()
    context = {
        'cat_list': cat_list,
        'tag_list': tag_list,
        'posts': paginate_posts(request=request, posts=posts, num=10),
    }
    return render(request, "blog/index.html", context=context)


def view_one_article(request, pk, slug):
    meta = BlogEntry.objects.get(pk=pk)
    post = Post.objects.get(slug=slug)
    # Last 3 posts
    last_posts = BlogEntry.objects.all().filter(status=PUBLISHED).filter(category=meta.category).exclude(
        post__slug=slug).order_by('-pub_date')[:3]

    # Get one breaking news
    breaking_news = BreakingNews.objects.all().filter(is_active=True).order_by('?')[:1]
    header_color = generate_rgba_color()
    context = {
        'post': post,
        'meta': meta,
        'related_posts': last_posts,
        'header_color': header_color,
    }
    if breaking_news:
        context['breaking_news'] = breaking_news[0]

    print(breaking_news)
    return render(request=request, template_name='blog/articles_details.html', context=context)


def category_details(request, slug):
    category = Category.objects.get(slug__iexact=slug)
    posts = BlogEntry.objects.all().filter(category=category).order_by('-updated_at')
    context = {
        'category': category,
        'posts': paginate_posts(request=request, posts=posts, num=10),
    }
    return render(request, 'blog/category.html', context=context)


@login_required(login_url='/admin/')
def add_category(request):
    form = AddCategoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_all_category')
    context = {
        'form': form,
        'button': 'Add Category',
        'page_title': 'Add Category',
    }
    return render(request, 'blog/add_category.html', context=context)


@login_required(login_url='/admin/')
def update_category(request, pk):
    category = Category.objects.get(pk=pk)
    form = AddCategoryForm(request.POST or None, instance=category)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_all_category')
    context = {
        'form': form,
        'button': 'Edit Category',
        'page_title': 'Edit Category',
    }
    return render(request, 'blog/add_category.html', context=context)


def view_all_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/list_tags_or_category.html', context=context)


@login_required(login_url='/admin/')
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('blog:view_all_category')
    except Category.DoesNotExist:
        return redirect('blog:view_all_category')


def tag_details(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    posts = tag.posts.all().order_by('-updated_at')
    context = {
        'tag': tag,
        'posts': paginate_posts(request=request, posts=posts, num=10),
    }
    return render(request, 'blog/tags.html', context=context)


@login_required(login_url='/admin/')
def add_tag(request):
    form = AddTagForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_all_tags')
    context = {
        'form': form,
        'button': 'Add Tag',
        'page_title': 'Add Tag',
    }
    return render(request, 'blog/add_tag.html', context=context)


@login_required(login_url='/admin/')
def update_tag(request, pk):
    tag = Tag.objects.get(pk=pk)
    form = AddTagForm(request.POST or None, instance=tag)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_all_tags')
    context = {
        'form': form,
        'button': 'Edit Tag',
        'page_title': 'Edit Tag',
    }
    return render(request, 'blog/add_tag.html', context=context)


def view_all_tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'blog/list_tags_or_category.html', context=context)


@login_required(login_url='/admin/')
def delete_tag(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return redirect('blog:view_all_tags')
    except Tag.DoesNotExist:
        return redirect('blog:view_all_tags')


def search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(status=PUBLISHED).filter(
        Q(title__icontains=query) | Q(snippet__icontains=query) | Q(body__icontains=query))
    context = {
        'posts': paginate_posts(request=request, posts=posts, num=10),
        'query': query,
    }
    return render(request, 'blog/search.html', context=context)
