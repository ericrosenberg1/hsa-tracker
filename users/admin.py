from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FamilyMember

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   list_display = ('email', 'is_staff', 'is_active')
   list_filter = ('is_staff', 'is_active')
   ordering = ('email',)
   search_fields = ('email',)

   fieldsets = (
       (None, {'fields': ('email', 'password')}),
       ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
   )
   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
       }),
   )

class FamilyMemberAdmin(admin.ModelAdmin):
   list_display = ('name', 'relationship', 'user', 'date_added')
   list_filter = ('relationship',)
   search_fields = ('name', 'relationship')
   ordering = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)