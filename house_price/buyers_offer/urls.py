from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offerform/', views.offer_form, name='offerform'),
    path('offerformconfirm/', views.offer_form_confirm, name='offerformconfirm'),
    path('offerform1/', views.offer_form_1, name='offerform1'),
    path('offerformconfirm1/', views.offer_form_confirm_1, name='offerformconfirm1')
]