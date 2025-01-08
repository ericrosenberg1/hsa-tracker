from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, HSAExpense

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   list_display = ('username', 'email', 'is_staff', 'is_family_member', 'family_name')
   list_filter = ('is_staff', 'is_family_member')
   fieldsets = UserAdmin.fieldsets + (
       ('Family Information', {'fields': ('is_family_member', 'family_name', 'relationship', 'bio')}),
   )
   add_fieldsets = UserAdmin.add_fieldsets + (
       ('Family Information', {'fields': ('is_family_member', 'family_name', 'relationship', 'bio')}),
   )

class HSAExpenseAdmin(admin.ModelAdmin):
   list_display = ('payee', 'expense_date', 'total', 'category', 'family_member')
   list_filter = ('category', 'expense_date', 'family_member')
   search_fields = ('payee', 'notes')
   date_hierarchy = 'expense_date'
   ordering = ('-expense_date',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HSAExpense, HSAExpenseAdmin)