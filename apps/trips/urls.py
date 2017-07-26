from django.conf.urls import url
from . import views
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<trip_id>\d+)/$', views.show, name='show'),
    # url(r'^(?P<trip_id>\d+)/edit/$', views.edit, name='edit'),
    # url(r'^(?P<trip_id>\d+)/update/$', views.update, name='update'),
    # url(r'^(?P<trip_id>\d+)/destroy/$', views.destroy, name='destroy'),
    url(r'^(?P<trip_id>\d+)/join/$', views.join, name='join'),
]
