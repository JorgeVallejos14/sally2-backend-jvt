from django.urls import path
from . import views

app_name = 'cartelera'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('espectaculo/<int:id>/', views.detalle, name='detalle'),
    path('ticket/<str:codigo>/', views.ticket, name='ticket'),
]