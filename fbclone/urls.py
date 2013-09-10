from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'fbclone_app.views.index'), # root
	url(r'^login', 'fbclone_app.views.login_view'), # login
	url(r'^logout$', 'fbclone_app.views.logout_view'), # logout
	url(r'^signup$', 'fbclone_app.views.signup'), # signup
)