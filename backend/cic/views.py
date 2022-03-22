from django.shortcuts import render


def index(request):
    """Home view callable, for the home page."""
    return render(request, 'index.html')
