from django.contrib import admin
from accounts.models import Address, CustomerUser, Follower


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    empty_value_display = 'Adresse inconue'
    list_display = ['email', 'get_full_name', 'is_active', 'is_staff']
    list_editable = ['is_active']

    # filters
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['address']
    filter_horizontal = ['groups', 'user_permissions']
    list_per_page = 10


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['following', 'followed']
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer_user', 'city', 'neighborhood', 'street', 'number']
    search_fields = ['city', 'street']
    # filter
    list_filter = ['city']
    search_fields = ['city']
    list_per_page = 10
