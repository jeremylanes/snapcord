from django.contrib import admin

from messaging.models import Group, Message, Recipient


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slogan', 'creation_date']
    list_per_page = 10
    search_fields = ['name', 'slogan']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    pass
