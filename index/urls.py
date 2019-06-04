from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('post_form/', views.post_form),
    path('getInfo/<int:id>/', views.getInfo),
    path('success/<int:id>/', views.qrcode)
]
