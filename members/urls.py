from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('register/', views.MemberCreateView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.MemberUpdateView.as_view(), name='profile_edit'),
    path('account-card/', views.account_card, name='account_card'),
    path('print-card/', views.account_card, name='print_card'),  # Alternative URL
    path('<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member_update'),
    path('registration-success/', views.registration_success, name='registration_success'),
]
