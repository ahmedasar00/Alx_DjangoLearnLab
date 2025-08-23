from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Comment


# Let's create a custom admin class for the Post model as well
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    list_filter = ("published_date", "author")
    search_fields = ("title", "content")


class CommentAdmin(admin.ModelAdmin):
    # 1. Define the columns to display in the list
    list_display = ("author", "post", "created_at", "edit_button", "delete_button")

    # 2. Make the 'post' field a filter in the sidebar
    list_filter = ("created_at", "post")

    # 3. Add a search bar
    search_fields = ("content", "author__username", "post__title")

    def get_edit_url(self, obj):
        return reverse("admin:blog_comment_change", args=[obj.pk])

    def get_delete_url(self, obj):
        return reverse("admin:blog_comment_delete", args=[obj.pk])

    # 4. Create a custom method for the Edit button
    def edit_button(self, obj):
        url = self.get_edit_url(obj)
        return format_html('<a class="button" href="{}">Edit</a>', url)

    edit_button.short_description = "Edit Comment"  # Column header

    # 5. Create a custom method for the Delete button
    def delete_button(self, obj):
        url = self.get_delete_url(obj)
        return format_html(
            '<a class="button" href="{}" style="background-color: #ba2121;">Delete</a>',
            url,
        )

    delete_button.short_description = "Delete Comment"  # Column header


# Register your models with their custom admin classes
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
