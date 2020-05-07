from bboard.views import index
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bboard/', include('bboard.urls', namespace='')),
    path('api/', include('api.urls')),
]
