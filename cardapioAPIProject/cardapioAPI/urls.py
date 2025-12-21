"""
URL configuration for cardapioAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cardapio.views import ItemViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# Health check endpoint for Railway
def health_check(request):
    return JsonResponse({"status": "healthy"})

# Temporary endpoint to create superuser - REMOVE AFTER USE!
def create_superuser_once(request):
    User = get_user_model()
    username = 'gustavocbrl'
    email = 'gustavo.zaidancabral@gmail.com'
    password = 'Dimitri22@'
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": f"User {username} already exists!"}, status=400)
    
    User.objects.create_superuser(username=username, email=email, password=password)
    return JsonResponse({"success": f"Superuser {username} created successfully! Now DELETE this endpoint."})

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('health/', health_check, name='health'),
    path('create-super-admin-once/', create_superuser_once, name='create_superuser'),  # TEMPORARY - REMOVE AFTER USE
    path('admin/', admin.site.urls),
    path('', include('cardapio.urls')),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root='static/')
