from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'fbclone_app.views.index'), # root
	url(r'^login', 'fbclone_app.views.login_view'), # login
	url(r'^logout$', 'fbclone_app.views.logout_view'), # logout
	url(r'^signup$', 'fbclone_app.views.signup'), # signup
	url(r'^newsfeed$', 'fbclone_app.views.newsfeed'), # newsfeed
	url(r'^submit$', 'fbclone_app.views.submit'), # share something
	url(r'^users/$', 'fbclone_app.views.users'), # see users
	url(r'^users/(?P<username>\w{0,50})/$', 'fbclone_app.views.users'),
	url(r'^friend$', 'fbclone_app.views.friend'), # add a friend
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
	url(r'^static/(?P<path>.*)$', 'serve'),
)
