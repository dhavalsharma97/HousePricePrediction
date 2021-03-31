from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('sellerscounterform/', views.sellers_counter_form, name='sellerscounterform'),
    path('sellerscounterform1/', views.sellers_counter_form_1, name='sellerscounterform1'),
    path('sellerscounterformconfirm/', views.counter_form_confirm, name='sellerscounterformconfirm'),
    path('sellerscounterformerror/', views.sellers_counter_form_error, name='sellerscounterformerror'),
    url(r'^sellerscounteroffersigningurl/$', views.embedded_signing_ceremony, name='sellerscounteroffersigningurl'),
    url(r'^sellerscounterofferaccesscode/$', views.get_access_code, name='sellerscounterofferaccesscode'),
    url(r'^sellerscounterofferaccesscode1/$', views.get_access_code_1, name='sellerscounterofferaccesscode1'),
    url(r'^sellerscounterofferauthlogin/$', views.auth_login, name='sellerscounterofferauthlogin'),
    url(r'^sellerscounterofferauthlogin1/$', views.auth_login_1, name='sellerscounterofferauthlogin1'),
    url(r'^sellerscounteroffersigncompleted/$', views.sign_completed, name='sellerscounteroffersigncompleted'),
    path('sellerscounteroffersigncomplete/', views.sign_complete, name='sellerscounteroffersigncomplete')
]