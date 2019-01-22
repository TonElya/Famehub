from django.conf.urls import url
from . import views


urlpatterns = [
    #url(r'^signup/', views.CreatePatronView.as_view(), name='signup'),
    #url(r'^email_verification/(?P<email_token>[^/]+)/', views.email_verification),
    #url(r'^email_verification/$',views.email_verification, name='email_verification'),
    #url(r'^email_us/', views.email_us),
    #url(r'^para/', views.para),
    url(r'^$', views.UserListView.as_view(), name='home'),
    #url(r'^user/(?P<pk>[-\w]+)/$', views.UserDetailView.as_view(), name='user-detail'),
    #url(r'^create_users/', views.create_users),
    #url(r'^reset_password/(?P<reset_token>[^/]+)/', views.reset_password),
    #url(r'^reset_password/', views.reset_password),
    #url(r'^create_user/', views.CreateRetailerView.as_view(), name='create_user')
    #path('login/',  views.LoginView.as_view(), name='login'),
]
