from django.contrib import admin
from django.urls import path, include
from users.views import home  # Import the home view from the users app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Root URL points to the home view
]
