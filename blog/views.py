from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from blog.models import BlogPost as Post, Tag, PUBLISHED, BlogEntry, Category, BreakingNews
from blog.utils import generate_rgba_color


def get_context_data(request):
    if request.user.is_authenticated:
        post_user_logged = BlogEntry.objects.all().order_by('-pub_date')
        return post_user_logged
    else:
        post = BlogEntry.objects.all().filter(status=PUBLISHED).order_by('-pub_date')
        return post


def view_all_article(request):
    posts = get_context_data(request=request)
    # Paginate posts
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    cat_list = Category.objects.all()
    tag_list = Tag.objects.all()
    context = {
        'cat_list': cat_list,
        'tag_list': tag_list,
        'posts': posts,
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


def category_detail(request, slug):
    category = Category.objects.get(slug__iexact=slug)
    posts = BlogEntry.objects.all().filter(category=category).order_by('-updated_at')
    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    posts = tag.posts.all().order_by('-updated_at')
    return render(request, 'blog/tags.html', {'tag': tag, 'posts': posts})


def search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(status=PUBLISHED).filter(
        Q(title__icontains=query) | Q(snippet__icontains=query) | Q(body__icontains=query))
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})
