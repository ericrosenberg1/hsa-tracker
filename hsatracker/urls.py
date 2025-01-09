from django.contrib import admin
from django.urls import path
from users import views as user_views
from expenses import views as expense_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Homepage and Dashboard
    path('', expense_views.dashboard, name='dashboard'),
    path('', user_views.home, name='home'),

    # Expense-related routes
    path('expenses/', expense_views.expense_list, name='expense_list'),
    path('expense/add/', expense_views.add_expense, name='add_expense'),
    path('expense/edit/<int:expense_id>/', expense_views.edit_expense, name='edit_expense'),
    path('expense/delete/<int:expense_id>/', expense_views.delete_expense, name='delete_expense'),

    # Family-related routes
    path('family/', expense_views.family, name='family'),
    path('family/add/', expense_views.add_family_member, name='add_family_member'),
    path('family/edit/<int:member_id>/', expense_views.edit_family_member, name='edit_family_member'),
    path('family/delete/<int:member_id>/', expense_views.delete_family_member, name='delete_family_member'),

    # User authentication and profile management
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('signup/', user_views.signup, name='signup'),
    path('profile/', user_views.profile, name='profile'),

    # Password management routes
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
