from django.urls import path
from .views import IndexView, calculate_subnet

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('calculate_subnet/', calculate_subnet, name='calculate_subnet'),
]
