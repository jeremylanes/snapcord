from django.contrib import admin

from publication.models import PostType, Filter, Post, PostMedia, Effect, Comment, Reaction


@admin.register(PostType)
class AdminPostType(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Filter)
class AdminFilter(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['user', 'type', 'creation_date']
    list_per_page = 10


@admin.register(PostMedia)
class AdminPostMedia(admin.ModelAdmin):
    list_display = ['post', 'filter']


@admin.register(Effect)
class AdminEffect(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'post', 'creation_date']
    list_per_page = 10


admin.register(Reaction)


@admin.register(Reaction)
class AdminReaction(admin.ModelAdmin):
    list_display = ['user', 'post']
