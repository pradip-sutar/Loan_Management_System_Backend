# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User

# class UserAdmin(BaseUserAdmin):
#     # Fields to display in the admin list view
#     list_display = ('username', 'is_active', 'is_staff', 'is_superuser', 'email', 'license_key', 'license_expiry', 'is_license_valid')

#     # Fields to filter by in the admin list view
#     list_filter = ('is_staff', 'is_superuser', 'is_active')

#     # Fields that can be searched in the admin
#     search_fields = ('username',)

#     # Fieldsets for organizing the user creation form
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions','email')}),
#     )

#     # Fields to display when adding a new user
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2'),
#         }),
#     )

#     # Ordering of the user list in admin
#     ordering = ('username',)

# # Register the custom User model with the custom UserAdmin
# admin.site.register(User, UserAdmin)
