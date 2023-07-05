from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('<str:slug>/', views.PageDetail.as_view(), name='page_slug'),
]
