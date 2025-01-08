from django.shortcuts import render

def home(request):
    return render(request, 'users/home.html')  # Renders the home.html template
