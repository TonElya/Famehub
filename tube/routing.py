from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/tube/(?P<room_name>[^/]+)/$', consumers.TubeConsumer),
]