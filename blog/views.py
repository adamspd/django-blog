from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from blog.forms import AddTagForm, AddCategoryForm, PostForm, PublishedPostForm, AddBreakingNewsForm, ContactForm
from blog.models import BlogPost as Post, Tag, PUBLISHED, DRAFT, BlogEntry, Category, BreakingNews
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
    return render(request, "blog/base/index.html", context=context)


def view_one_article(request, slug):
    post = Post.objects.get(slug=slug)
    meta = BlogEntry.objects.get(post=post)
    if meta.is_draft and not request.user.is_superuser:
        # return not found and redirect to home page
        return HttpResponseForbidden("You don't have permission to view this page")
    # Last 3 posts
    last_posts = BlogEntry.objects.all().filter(status=PUBLISHED).filter(category=meta.category).exclude(
        post__slug=slug).order_by('-pub_date')[:3]

    # if last_posts is empty then get last 3 posts from all posts
    if not last_posts:
        last_posts = BlogEntry.objects.all().filter(status=PUBLISHED).exclude(post__slug=slug).order_by('-pub_date')[:3]

    # Get one breaking news
    breaking_news = BreakingNews.objects.all().filter(is_active=True).order_by('?')[:1]
    header_color = generate_rgba_color()

    tag_list_query = list(post.tag.all())
    ids = set(existing_answer.id for existing_answer in tag_list_query)
    tag_list_as_list = [tag.name.replace("#", "") for tag in tag_list_query if tag.id in ids]
    tag_list = ', '.join(tag_list_as_list)

    context = {
        'post': post,
        'meta': meta,
        'related_posts': last_posts,
        'header_color': header_color,
        'tag_list': tag_list,
    }
    if breaking_news:
        context['breaking_news'] = breaking_news[0]

    print(breaking_news)
    return render(request=request, template_name='blog/post/articles_details.html', context=context)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:publish_article', pk=form.instance.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post/add_post.html', {'form': form})


@login_required(login_url='/admin/')
def update_article(request, pk):
    post = Post.objects.get(pk=pk)
    print(f"this is the post {post}")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:publish_article', pk=form.instance.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post/update_post.html', {'form': form})


@login_required(login_url='/admin/')
def publish_article(request, pk):
    post = Post.objects.get(pk=pk)
    form = PublishedPostForm(request.POST or None)
    if form.is_valid():
        try:
            meta = BlogEntry.objects.get(post=post)
            meta.status = form.cleaned_data['status']
            meta.category = form.cleaned_data['category']
            meta.save()
            return redirect('blog:article_details', slug=post.slug)
        except BlogEntry.DoesNotExist:
            meta = BlogEntry.objects.create(post=post, status=form.cleaned_data['status'],
                                            category=form.cleaned_data['category'])
            return redirect('blog:article_details', slug=post.slug)
    context = {
        'form': form,
        'page_title': 'Publish Post',
        'button_text': 'Publish',
    }
    return render(request, 'blog/post/publish_post.html', context=context)


@login_required(login_url='/admin/')
def publish_post(request, pk):
    BlogEntry.objects.filter(post__pk=pk).update(status=PUBLISHED)
    return redirect('blog:article_details', slug=Post.objects.get(pk=pk).slug)


@login_required(login_url='/admin/')
def unpublished_article(request, pk):
    BlogEntry.objects.filter(post__pk=pk).update(status=DRAFT)
    return redirect('blog:article_details', slug=Post.objects.get(pk=pk).slug)


@login_required(login_url='/admin/')
def delete_article(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:home')
    except Post.DoesNotExist:
        return redirect('blog:home')


def category_details(request, slug):
    category = Category.objects.get(slug__iexact=slug)
    if request.user.is_authenticated:
        posts = BlogEntry.objects.all().filter(category=category).order_by('-pub_date')
    else:
        posts = BlogEntry.objects.all().filter(category=category).filter(status=PUBLISHED).order_by('-updated_at')
    context = {
        'category': category,
        'posts': paginate_posts(request=request, posts=posts, num=10),
    }
    return render(request, 'blog/tags_categories/category.html', context=context)


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
    return render(request, 'blog/tags_categories/add_category.html', context=context)


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
    return render(request, 'blog/tags_categories/add_category.html', context=context)


def view_all_category(request):
    categories = Category.objects.all()
    context = {
        'page_title': 'All Categories',
        'categories': categories,
    }
    return render(request, 'blog/tags_categories/list_tags_or_category.html', context=context)


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
    if not request.user.is_superuser:
        posts = tag.posts.all().order_by('-updated_at').filter(blogentry__status=PUBLISHED)
    else:
        posts = tag.posts.all().order_by('-updated_at')
    context = {
        'tag': tag,
        'posts': paginate_posts(request=request, posts=posts, num=10),
    }
    return render(request, 'blog/tags_categories/tags.html', context=context)


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
    return render(request, 'blog/tags_categories/add_tag.html', context=context)


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
    return render(request, 'blog/tags_categories/add_tag.html', context=context)


def view_all_tags(request):
    tags = Tag.objects.all()
    context = {
        'page_title': "All Tags",
        'tags': tags,
    }
    return render(request, 'blog/tags_categories/list_tags_or_category.html', context=context)


@login_required(login_url='/admin/')
def delete_tag(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return redirect('blog:view_all_tags')
    except Tag.DoesNotExist:
        return redirect('blog:view_all_tags')


def view_breaking_news(request):
    breaking_news = BreakingNews.objects.all().order_by('-updated_at')
    context = {
        'breaking_news': breaking_news,
    }
    return render(request, 'blog/breaking_news/view.html', context=context)


def details_breaking_news(request, pk):
    breaking_news = BreakingNews.objects.get(pk=pk)
    context = {
        'breaking_news': breaking_news,
    }
    return render(request, 'blog/breaking_news/details.html', context=context)


@login_required(login_url='/admin/')
def add_breaking_news(request):
    form = AddBreakingNewsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_breaking_news')
    context = {
        'form': form,
        'button': 'Add Breaking News',
        'page_title': 'Add Breaking News',
    }
    return render(request, 'blog/breaking_news/add.html', context=context)


@login_required(login_url='/admin/')
def update_breaking_news(request, pk):
    breaking_news = BreakingNews.objects.get(pk=pk)
    form = AddBreakingNewsForm(request.POST or None, instance=breaking_news)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:view_breaking_news')
    context = {
        'form': form,
        'button': 'Edit Breaking News',
        'page_title': 'Edit Breaking News',
    }
    return render(request, 'blog/breaking_news/add.html', context=context)


@login_required(login_url='/admin/')
def delete_breaking_news(request, pk):
    try:
        breaking_news = BreakingNews.objects.get(pk=pk)
        breaking_news.delete()
        return redirect('blog:view_breaking_news')
    except BreakingNews.DoesNotExist:
        return redirect('blog:view_breaking_news')


def search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(blogentry__status=PUBLISHED).filter(
        Q(title__icontains=query) | Q(headline__icontains=query) | Q(content__icontains=query))
    print(posts)
    context = {
        'posts': paginate_posts(request=request, posts=posts, num=10),
        'query': query,
    }
    return render(request, 'blog/base/search.html', context=context)


def sign_out(request):
    logout(request)
    return redirect('blog:home')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            hidden = form.cleaned_data['hidden']
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            if hidden != "":
                print(f"Bot detected: full name: {full_name}, email: {email}, message: {message}, bot: {hidden}")
                messages.success(request, "Your message has been sent successfully !")
                return redirect("homepage:contact")
            else:
                Contact.objects.create(full_name=full_name, email=email, message=message)
                print(f"form is valid and saved: {full_name}, {email}, {message}")
                messages.success(request, "Your message has been sent successfully !")
                return redirect('homepage:contact')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'blog/contact_legal/contact.html', context)
