from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import settings
from .views import home
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('members/', include('members.urls')),
    path('transactions/', include('transactions.urls')),
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
