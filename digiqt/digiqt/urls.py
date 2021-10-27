"""digiqt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import Home, Search

# Use from base dir namespace
html_dir = 'html/lte/'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ckeditor/', include('ckeditor_uploader.urls')),  # ckeditor related

    # web api
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include([
        path('celeb/', include('celebs.api.urls', namespace='celebs')),
        path('movie/', include('movies.api.urls', namespace='movies')),
        path('account/', include('users.api.urls'))
    ])),

    # data with HTML, no web api (no json data)
    # for api movies view http://127.0.0.1:8000/api/movie/
    path('', include([
        path('celeb/', include('celebs.urls')),
        path('movie/', include('movies.urls')),
        path(
            'search/', Search.as_view(template_name=html_dir + 'search.html'),
            name='search'),
        path(
            '', Home.as_view(template_name=html_dir + 'index.html'),
            name='index')
    ])),
]

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)



