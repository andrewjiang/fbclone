from django.conf.urls import patterns, include, url

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
)