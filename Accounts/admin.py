from django.contrib import admin
from . models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'date_joined', 'last_login', 'is_admin', 'is_superadmin') # display the email, username, first name, last name, phone number, date joined, last login, is admin, and is superadmin in the admin panel
    list_display_links = ('email', 'username', 'first_name', 'last_name') # make the email, first name, and last name clickable
    readonly_fields = ('date_joined', 'last_login') # make the date joined and last login fields read-only
    ordering = ('-date_joined',) # order the accounts by date joined in descending order

    filter_horizontal = () # remove the filter horizontal option
    list_filter = () # remove the list filter option
    fieldsets = () # remove the fieldsets option

admin.site.register(Account, AccountAdmin) # register the Account model with the AccountAdmin class