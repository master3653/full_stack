from django.conf.urls import url
from django.contrib.auth.views import login
# With django 1.10 I need to pass the callable instead of
# url(r'^login/$', 'django.contrib.auth.views.login', name='login')

from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from . import views

urlpatterns = [
    #url(r'^login/$',views.user_login,name='login'),
    #url(r'^logout/$','django.contrib.auth.views.logout',name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$','django.contrib.auth.views.logout_then_login',name='logout_then_login'),
# change password
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    # reset password
    ## restore password urls
    url(r'^password-reset/$',password_reset,name='password_reset'),
    url(r'^password-reset/done/$',password_reset_done,name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',password_reset_confirm,name='password_reset_confirm'),
    url(r'^password-reset/complete/$',password_reset_complete,name='password_reset_complete'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^register/$',views.register,name='register'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^oauth/qq/login', views.qq_login, name='qq_login'),
    url(r'^oauth/qq/check', views.qq_check, name='qq_check'),
    url(r'^oauth/bind/account', views.bind_account, name='bind_account'),
    url(r'^users/$',views.user_list,name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='follow'),  # follow必须放在detail前面
    url(r'^users/(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),



]