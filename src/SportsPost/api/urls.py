from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import (
			LikeToggleAPIView,
			ReshareAPIView,
			SportsListAPIView,
			SportCreateAPIView,
			SportDetailAPIView,
			)

app_name = 'postsports-api'

urlpatterns = [
	# url(r'^$', RedirectView.as_view(url="/")),
    url(r'^$', SportsListAPIView.as_view(), name='list'),
    url(r'^create/$', SportCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', SportDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='reshare'),
    url(r'^(?P<pk>\d+)/reshare/$', ReshareAPIView.as_view(), name='like-toggle'),
 #    url(r'^(?P<pk>\d+)/$', SportsPostDetailView.as_view(), name='detail'),
 #    url(r'^(?P<pk>\d+)/update/$', SportsPostUpdateView.as_view(), name='update'),
 #    url(r'^(?P<pk>\d+)/delete/$', SportsPostDeleteView.as_view(), name='delete')
] 
