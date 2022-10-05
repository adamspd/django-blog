# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogEntry as Post


class BlogViewSitemap(Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return Post.objects.all().filter(status='published')

    def lastmod(self, obj):
        return obj.pub_date
