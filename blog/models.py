from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown2 import markdown

from blog.utils import get_read_time, generate_3_backgrounds_colors, generate_rgba_color, generate_rgb_color

PUBLISHED = 'published'
DRAFT = 'draft'

CHOICE_STATUS = (
    (PUBLISHED, 'Published'),
    (DRAFT, 'Draft')
)


class Tag(models.Model):
    """A tag can be #docker, #ubuntu or #kubernetes which is different from a category."""
    name = models.CharField(max_length=255, default="#", )
    slug = models.SlugField(max_length=150, null=True, blank=True, default="")
    tag_color = models.CharField(max_length=255, default=generate_rgba_color, null=True, blank=True)

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves the tag and create a slug from the name."""
        if not self.slug:
            self.slug = slugify(self.name)
        self.tag_color = generate_rgb_color()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})


class Category(models.Model):
    """A blog category, can be Technology, Coding, Programming which is different from a tag."""
    name = models.CharField(max_length=100, null=True, blank=False, default="")
    slug = models.SlugField(max_length=150, null=True, blank=True, default="")
    category_color = models.CharField(max_length=255, default=generate_rgba_color, null=True, blank=True)

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves the tag and create a slug from the name."""
        if not self.slug:
            self.slug = slugify(self.name)
        self.tag_color = generate_rgb_color()
        return super().save(*args, **kwargs)

    # def get_update_url(self):
    #     return reverse('blog:article_update', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class BlogPost(models.Model):
    """
    Stores a single all the content of a blog post. related to :model:`auth.User`
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    header_img = models.CharField(null=True, blank=True,
                                  default="background: rgba(238, 174, 202, 1); background: radial-gradient(circle, "
                                          "rgba(238, 174, 202, 1) 0%, rgba(148, 187, 233, 1) 100%);",
                                  max_length=255)
    header_color = models.CharField(null=True, blank=True, default="#67d1fb", max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    headline = models.CharField(max_length=255, default="")
    table_content = RichTextField(default="", blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, help_text="A short label, generally used in URLs.")
    tag = models.ManyToManyField('Tag', blank=True, related_name='posts')
    reading_time = models.IntegerField(null=True, blank=True, default=0)

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Saves the blog content and automatically create a slug from the title."""
        if not self.slug:
            self.slug = slugify(self.title)
        if self.content:
            html_string = self.get_markdown()
            read_time = get_read_time(html_string)
            self.reading_time = read_time
            print("read time is ", read_time)
        self.header_img = generate_3_backgrounds_colors()
        self.header_color = generate_rgba_color()
        return super().save(*args, **kwargs)

    def get_markdown(self):
        """Convert the html to markdown."""
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_absolute_url(self):
        return reverse('blog:article_details', kwargs={'pk': self.pk, 'slug': self.slug})


class BlogEntry(models.Model):
    """
    Stores a single blog entry, related to :model:`blog.BlogPost` and
    :model:`blog.Category`.
    """
    post = models.ForeignKey(BlogPost, models.CASCADE)
    pub_date = models.DateField()
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default=DRAFT)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.post.title + ' | ' + self.post.author.get_full_name()

    @property
    def is_published(self):
        """:return if blog entry is active"""
        if self.status == PUBLISHED:
            return True

    @property
    def is_draft(self):
        """:return if blog entry is inactive."""
        if self.status == DRAFT:
            return True

    @property
    def get_status(self):
        """:return blog entry status."""
        return self.status

    def save(self, *args, **kwargs):
        """Saves the blog entry. Removes the published date if blog post is inactive."""
        if self.is_draft:
            self.pub_date = None
        return super().save(*args, **kwargs)

    def publish(self):
        """Makes the blog entry live on the site."""
        self.status = PUBLISHED
        self.save()

    def unpublished(self):
        """Removes the blog entry on the site."""
        self.status = DRAFT
        self.save()

    # def get_absolute_url(self):
    #     return reverse('blog:article_details', args=(str(self.id), self.slug))


class PostImage(models.Model):
    """Stores all images that can be reused in any blog post content."""
    name = models.CharField(max_length=255, default="")
    files = models.FileField(upload_to="posts")

    def __str__(self):
        return self.name


class TemplateConfiguration(models.Model):
    use_blog_menu = models.BooleanField(default=False)
    use_blog_footer = models.BooleanField(default=False)
    use_base_js = models.BooleanField(default=False)
    copyright = models.CharField(default="Adams Pierre David &copy;", max_length=255)
    site_description = models.CharField(
        default="Author: Adams Pierre David, Designer: Adams Pierre David, Category: Blog",
        max_length=255)


class BreakingNews(models.Model):
    title = models.CharField(max_length=255, default="")
    content = models.TextField(default="")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            BreakingNews.objects.filter(is_active=True).update(is_active=False)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Breaking News"
