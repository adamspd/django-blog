from django.contrib import admin

from blog.models import BlogPost, Tag, PostImage, BlogEntry, Category, TemplateConfiguration, BreakingNews, Contact


@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content', 'headline']
    list_display = ("title", "headline",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogEntry)
class PostEntryAdmin(admin.ModelAdmin):
    search_fields = ['post', 'pub_date', 'status', 'category', 'created_at', 'updated_at']
    list_display = ("post", "pub_date", 'status', 'category', 'created_at', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(TemplateConfiguration)
class TemplateConfigurationAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakingNews)
class BreakingNewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactForm(admin.ModelAdmin):
    model = Contact
    search_fields = ('full_name', 'email', 'message', 'date_created')
    list_filter = ('date_created', 'full_name', 'email')
    ordering = ('-date_created',)
    list_display = ('full_name', 'date_created', 'email')


