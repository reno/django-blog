from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Post, Comment


admin.site.unregister(Group)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
    list_display = ['title', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'text']
    list_filter = ['author']
    inlines = [CommentInline]
