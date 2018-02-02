from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'login/',views.login_view,name='login'),
    url(r'reg/',views.register_view,name='reg'),
    url(r'edit/',views.update_user_bduss,name='edit'),
    url(r'refbd/',views.add_user_tieba,name='refbd'),
    url(r'logout',views.logout_view,name='logout'),
]