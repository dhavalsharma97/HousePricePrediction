from django.urls import path
from django.conf.urls import url
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
    path('offerformconfirm3/', views.offer_form_confirm_3, name='offerformconfirm3'),
    path('offerform4/', views.offer_form_4, name='offerform4'),
    path('offerformconfirm4/', views.offer_form_confirm_4, name='offerformconfirm4'),
    path('offerformnavigate/', views.offer_form_navigate, name='offerformnavigate'),
    url(r'^buyersoffersigningurl/$', views.embedded_signing_ceremony, name='buyersoffersigningurl'),
    url(r'^buyersofferaccesscode/$', views.get_access_code, name='buyersofferaccesscode'),
    url(r'^buyersofferauthlogin/$', views.auth_login, name='buyersofferauthlogin'),
    url(r'^offerformsigncompleted/$', views.sign_completed, name='offerformsigncompleted'),
    path('offerformsigncomplete/', views.sign_complete, name='offerformsigncomplete')
]