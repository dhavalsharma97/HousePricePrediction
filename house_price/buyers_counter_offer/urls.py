from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('buyerscounterform/', views.buyers_counter_form, name='buyerscounterform'),
    path('buyerscounterform1/', views.buyers_counter_form_1, name='buyerscounterform1'),
    path('buyerscounterform2/', views.buyers_counter_form_2, name='buyerscounterform2'),
    path('buyerscounterformconfirm/', views.counter_form_confirm, name='buyerscounterformconfirm'),
    path('buyerscounterformerror/', views.buyers_counter_form_error, name='buyerscounterformerror'),
    url(r'^buyerscounteroffersigningurl/$', views.embedded_signing_ceremony, name='buyerscounteroffersigningurl'),
    url(r'^buyerscounterofferaccesscode/$', views.get_access_code, name='buyerscounterofferaccesscode'),
    url(r'^buyerscounterofferaccesscode1/$', views.get_access_code_1, name='buyerscounterofferaccesscode1'),
    url(r'^buyerscounterofferauthlogin/$', views.auth_login, name='buyerscounterofferauthlogin'),
    url(r'^buyerscounterofferauthlogin1/$', views.auth_login_1, name='buyerscounterofferauthlogin1'),
    url(r'^buyerscounteroffersigncompleted/$', views.sign_completed, name='buyerscounteroffersigncompleted'),
    path('buyerscounteroffersigncomplete/', views.sign_complete, name='buyerscounteroffersigncomplete')
]