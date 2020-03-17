from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^delete/(?P<city_id>[0-9]+)/(?P<list_id>[0-9]+)/$', views.delete_city, name='delete_city'),
    url(r'^add_schedule/(?P<schedule_id>[0-9]+)/(?P<list_id>[0-9]+)/$', views.add_schedule, name='add_schedule'),
]
