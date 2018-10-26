from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import (
			ReshareView,
			SportsPostDetailView, 
			SportsPostDeleteView,
			SportsPostListView, 
			SportsPostCreateView,
			SportsPostUpdateView
			)

app_name = 'postsports'
app_name = 'postsports-api'
app_name = 'profiles'

urlpatterns = [
	url(r'^$', RedirectView.as_view(url="/")),
    url(r'^search/$', SportsPostListView.as_view(), name='list'),
    url(r'^create/$', SportsPostCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', SportsPostDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/reshare/$', ReshareView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', SportsPostUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', SportsPostDeleteView.as_view(), name='delete')
] 
