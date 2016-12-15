from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^homepage/$', views.homepage),
    url(r'^log_out/$', views.log_out),
    url(r'^homepage/add/$', views.add_book_review),
    url(r'^homepage/add/process/$', views.process_book),
    url(r'^homepage/(?P<id>\d*)/$', views.go_to_book),
    url(r'^homepage/(?P<id>\d*)/process/$', views.new_review),
    url(r'^user/(?P<id>\d*)/$', views.user),
]
