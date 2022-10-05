import random

from django.db.models import Q
from django.shortcuts import render

from blog.models import BlogPost as Post, Tag, PUBLISHED, BlogEntry, Category, BreakingNews


def get_context_data(request):
    if request.user.is_authenticated:
        post_user_logged = BlogEntry.objects.all().order_by('-pub_date')
        return post_user_logged
    else:
        post = BlogEntry.objects.all().filter(status=PUBLISHED).order_by('-pub_date')
        return post


def filter_all_article_context(post_list, context):
    if len(post_list) >= 5:
        last_post = post_list[0]
        first_row = post_list[1:4]
        the_rest = post_list[4:]
    elif 5 > len(post_list) > 1:
        last_post = post_list[0]
        first_row = post_list[1:4]
        the_rest = None
    elif len(post_list) == 1:
        last_post = post_list[0]
        first_row = None
        the_rest = None
    else:
        last_post = None
        first_row = None
        the_rest = None
    context["first_entry"] = last_post
    context["row"] = first_row
    context["rest"] = the_rest
    return context


def view_all_article(request):
    posts = get_context_data(request=request)
    cat_list = Category.objects.all()
    tag_list = Tag.objects.all()
    context = {
        'cat_list': cat_list,
        'tag_list': tag_list,
    }
    context = filter_all_article_context(post_list=posts, context=context)
    return render(request, "blog/index.html", context=context)


def view_one_article(request, pk, slug):
    meta = BlogEntry.objects.get(pk=pk)
    post = Post.objects.get(slug=slug)
    # Last 3 posts
    last_posts = BlogEntry.objects.all().filter(status=PUBLISHED).filter(category=meta.category).exclude(
        post__slug=slug).order_by('-pub_date')[:3]

    # Get one breaking news
    breaking_news = BreakingNews.objects.all().filter(is_active=True).order_by('?')[:1]
    context = {
        'post': post,
        'meta': meta,
        'related_posts': last_posts,
    }
    if breaking_news:
        context['breaking_news'] = breaking_news[0]

    print(breaking_news)
    return render(request=request, template_name='blog/articles_details_new.html', context=context)


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    posts = tag.posts.all().order_by('-date_published')
    return render(request, 'blog/tags.html', {'tag': tag, 'posts': posts})


def search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(status=PUBLISHED).filter(
        Q(title__icontains=query) | Q(snippet__icontains=query) | Q(body__icontains=query))
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})

