from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.contrib import messages

class SuperuserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that should be accessible without being a superuser
        exempt_paths = [
            reverse('accounts:login'), 
            '/admin/login/',
            '/admin/'
        ]
        
        # Allow access to static and media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
            
        # Allow access to the admin login page and exempt paths
        if request.path in exempt_paths or request.path.startswith('/admin/'):
            return self.get_response(request)
            
        # Check if the user is authenticated and is a superuser
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему для доступа к этой странице.')
            return redirect('accounts:login')
            
        if not request.user.is_superuser:
            messages.error(request, 'Доступ разрешен только для суперпользователя.')
            return redirect('accounts:login')
            
        return self.get_response(request) 