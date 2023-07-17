from django.urls import path
from .views import api
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('<str:slug>/', views.PageDetail.as_view(), name='page_slug'),

    path('api/sidebar/<int:state>/', api.sidebar_state, name='api_sidebar_state'),
]
