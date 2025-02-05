from django.contrib import admin
from core import settings
from .views import home
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('members/', include('members.urls')),
    path('admin/', admin.site.urls),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
