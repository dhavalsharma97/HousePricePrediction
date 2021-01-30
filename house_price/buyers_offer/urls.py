from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offerform/', views.offer_form, name='form'),
    path('offerformconfirm/', views.offer_form_confirm, name='offerformconfirm')
]