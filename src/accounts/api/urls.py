from django.conf.urls import url

from django.views.generic.base import RedirectView

from SportsPost.api.views import (
			SportsListAPIView,
			)

app_name = 'postsports'
app_name = 'postsports-api'
app_name = 'profiles'
app_name = 'profiles-api'


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/qspost/$', SportsListAPIView.as_view(), name='list'),
] 

