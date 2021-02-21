from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offerform/', views.offer_form, name='offerform'),
    path('offerformconfirm/', views.offer_form_confirm, name='offerformconfirm'),
    path('offerform1/', views.offer_form_1, name='offerform1'),
    path('offerformconfirm1/', views.offer_form_confirm_1, name='offerformconfirm1'),
    path('offerform2/', views.offer_form_2, name='offerform2'),
    path('offerformconfirm2/', views.offer_form_confirm_2, name='offerformconfirm2'),
    path('offerform3/', views.offer_form_3, name='offerform3'),
    path('offerformconfirm3/', views.offer_form_confirm_3, name='offerformconfirm3')
]