from django.contrib import admin
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import UserRegister
from hashtags.views import HashTagView
from SportsPost.api.views import SearchSportsAPIView
from SportsPost.views import SportsPostListView
from .views import home, SearchView


app_name = 'postsports'
app_name = 'postsports-api'
app_name = 'profiles'
app_name = 'profiles-api'
app_name = 'register'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SportsPostListView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^api/search/$', SearchSportsAPIView.as_view(), name='search-api'),
    url(r'^tags/(?P<hashtag>.*)/$', HashTagView.as_view(), name='hashtag'),
    url(r'^qspost/', include('SportsPost.urls', namespace='postsports')),
    url(r'^api/qspost/', include('SportsPost.api.urls', namespace='postsports-api')),
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
    url(r'^register/$', UserRegister.as_view(), name='register'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('accounts.urls', namespace='profiles')),
] 

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
