from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('6889/', views.sixty_eight)
]