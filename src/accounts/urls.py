from django.conf.urls import url, include

from django.views.generic.base import RedirectView

from .views import (
			UserDetailView,
			UserFollowView
			)

app_name = 'profiles'

urlpatterns = [
 # 	  url(r'^$', RedirectView.as_view(url="/")),
 #    url(r'^search/$', SportsPostListView.as_view(), name='list'),
 #    url(r'^create/$', SportsPostCreateView.as_view(), name='create'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow$', UserFollowView.as_view(), name='follow'),
 #    url(r'^(?P<pk>\d+)/update/$', SportsPostUpdateView.as_view(), name='update'),
 #    url(r'^(?P<pk>\d+)/delete/$', SportsPostDeleteView.as_view(), name='delete')
] 
