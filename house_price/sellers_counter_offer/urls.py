from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('sellerscounterform/', views.sellers_counter_form, name='sellerscounterform'),
    path('sellerscounterform1/', views.sellers_counter_form_1, name='sellerscounterform1'),
    path('counterformconfirm/', views.counter_form_confirm, name='counterformconfirm'),
    path('sellerscounterformerror/', views.sellers_counter_form_error, name='sellerscounterformerror'),
    url(r'^get_access_code/$', views.get_access_code, name='getaccesscode'),
    url(r'^auth_login/$', views.auth_login, name='authlogin'),
]