"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

from blog.views import *

app_name = 'blog'

# Extra patterns
category_patterns = [
    path('add/', add_category, name='add_category'),
    path('details/<slug:slug>/', category_details, name='category_details'),
    path('list/', view_all_category, name='view_all_category'),
    path('update/<int:pk>/', update_category, name='update_category'),
    path('delete/<int:pk>/', delete_category, name='delete_category'),
]

tag_patterns = [
    path('add/', add_tag, name='add_tag'),
    path('details/<slug:slug>/', tag_details, name='tag_details'),
    path('list/', view_all_tags, name='view_all_tags'),
    path('update/<int:pk>/', update_tag, name='edit_tag'),
    path('delete/<int:pk>/', delete_tag, name='delete_tag'),
]

article_patterns = [
    path('<int:pk>/<slug:slug>/', view_one_article, name='article_details'),
    path('add/', add_article, name='add_article'),
    path('update/<int:pk>/', update_article, name='update_article'),
    path('delete/<int:pk>/', delete_article, name='delete_article'),
    path('publish-article/<int:pk>/', publish_article, name='publish_article'),
    path('publish/<int:pk>/', publish_post, name='publish'),
    path('unpublish/<int:pk>/', unpublished_article, name='unpublished'),
]

breaking_news_patterns = [
    path('add/', add_breaking_news, name='add_breaking_news'),
    path('details/<int:pk>/', details_breaking_news, name='breaking_news_details'),
    path('list/', view_breaking_news, name='view_breaking_news'),
    path('update/<int:pk>/', update_breaking_news, name='update_breaking_news'),
    path('delete/<int:pk>/', delete_breaking_news, name='delete_breaking_news'),
]

urlpatterns = [
    path('', view_all_article, name='home'),
    path('article/', include(article_patterns)),
    path('tag/', include(tag_patterns)),
    path('category/', include(category_patterns)),
    path('breaking-news/', include(breaking_news_patterns)),
    path('search/', search, name='search'),
    path('logout/', sign_out, name='logout'),
    path('contact/', contact, name='contact'),
]
