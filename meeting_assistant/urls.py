from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('zoomApp.urls')),  # Include URLs from the zoomApp
]
