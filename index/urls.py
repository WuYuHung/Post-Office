from django.urls import path

from . import views

urlpatterns = [
    path('6889/', views.sixty_eight),
    path('9091/', views.ninety)
]