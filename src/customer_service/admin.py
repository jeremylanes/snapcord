from django.contrib import admin

from customer_service.models import Message, BroadcastEmail


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'readed', 'author']
    list_editable = ['readed']
    empty_value_display = 'Inconu'
    # filters
    list_filter = ['readed']
    list_per_page = 10


@admin.register(BroadcastEmail)
class BroadcastEmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'broadcast', 'sending_date']
    list_editable = ['broadcast']
    list_filter = ['broadcast']
    list_per_page = 10
