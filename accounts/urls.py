from accounts import views
from django.urls import path

urlpatterns = [
    path('register/', views.registro, name='signup'),
]