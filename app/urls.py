from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logMeIn, name="login"),
    path('navigationAdm/', views.navigationAdm, name="navigationAdm"),
    path('navigationEmp/', views.navigationEmp, name="navigationEmp"),
    path('clientes/', views.clientes, name="clientes"),
    path('catalogo/', views.catalogo, name="catserv"),
    path('agenda/', views.agenda, name="agenda"),
    path('faturamento/', views.faturamento, name="faturamento")
]

urlpatterns += static(settings.MEDIA_URL, documento_root=settings.MEDIA_ROOT)