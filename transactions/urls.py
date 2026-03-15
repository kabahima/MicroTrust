from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('shares/', views.shares, name='shares'),
]