from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'login/',views.login_view,name='login'),
    url(r'reg/',views.register_view,name='reg'),
    url(r'edit/',views.edit_view,name='edit'),
    url(r'logout',views.logout_view,name='logout')
]