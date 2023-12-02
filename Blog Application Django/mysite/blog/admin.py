from django.contrib import admin
from .models import Post,PostComments

# Register your models here.
# admin.site.register(Post)

# lets customize the admin site to how to show the data
# use MondelAdmin decorators
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status','number_of_likes']
    list_filter=['status','created','publish','author']
    search_fields = ['author','slug']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status','publish']

    def number_of_likes(self, obj):
        return obj.number_of_like()
    number_of_likes.short_description = 'Number of Likes'


@admin.register(PostComments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post','created','active']
    list_filter=['active','created']