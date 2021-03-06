from django.conf.urls import url
from . import views


urlpatterns = [
#url(r'^create_all/$', views.create_lessons),
url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
#url(r'^video/like/(?P<video_id>[-\w]+)/$', views.like),
url(r'^video/api_like/(?P<video_id>[-\w]+)/$', views.api_like),
url(r'^video/api_unlike/(?P<video_id>[-\w]+)/$', views.api_unlike),
#url(r'^video/unlike/(?P<video_id>[-\w]+)/$', views.unlike),
    url(r'^video/(?P<pk>[-\w]+)/$', views.VideoDetailView.as_view(), name='video-detail'),

#url(r'^generate/pdf/$', views.generate_pdf, name='generate_pdf'),
   url(r'^$', views.VideoListView.as_view(), name='videos'),
    url(r'^create_video/', views.CreateVideoView.as_view(), name='create_video'),

  #  url(r'^lesson_tryit/', views.lesson_tryit),
   # url(r'^(?P<title>[^/]+)/$', views.redirect_lesson),
    #url(r'^email_verification/(?P<email_token>[^/]+)/', views.email_verification),
    #url(r'^email_us/', views.email_us),
    #url(r'^create_user/', views.CreateRetailerView.as_view(), name='create_user')
    #path('login/',  views.LoginView.as_view(), name='login'),

]

