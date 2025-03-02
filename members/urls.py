from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.MemberListView.as_view(), name='member_list'),
    path('members/add/', views.MemberCreateView.as_view(), name='member_create'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member_update'),
]
