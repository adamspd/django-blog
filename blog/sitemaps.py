# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import PUBLISHED, BlogPost, BlogEntry


class BlogViewSitemap(Sitemap):
    priority = 1
    changefreq = 'weekly'

    def items(self):
        return BlogPost.objects.all().filter(blogentry__status=PUBLISHED)

    def lastmod(self, obj):
        return obj.get_pub_date()
