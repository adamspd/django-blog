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

from django.urls import path

from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', view_all_article, name='home'),
    path('article/<int:pk>/<slug:slug>/', view_one_article, name='article_details'),
    # path('add-post/', CreateArticle.as_view(), name='add_post'),
    # path('article/edit/<int:pk>', UpdateArticle.as_view(), name='update_post'),
    # path('article/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    # path('add-tag/', AddTagView.as_view(), name='add_category'),
    path('category/<slug:slug>/', category_detail, name='category'),
    path('tag/<slug:slug>/', tag_detail, name='tag'),
]