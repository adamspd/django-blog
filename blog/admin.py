from django.contrib import admin

from blog.models import BlogPost, Tag, PostImage, BlogEntry, Category, TemplateConfiguration, BreakingNews


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
class PostPictureAdmin(admin.ModelAdmin):
    pass


@admin.register(TemplateConfiguration)
class PostPictureAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakingNews)
class PostPictureAdmin(admin.ModelAdmin):
    pass
