from django.urls import re_path

from . import views

app_name = 'simple_api_app'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^add_task/$', views.task, name='add_task'),
    re_path(r'^(?P<task_id>\d+)/edit_task/$', views.task, name='edit_task'),
    re_path(r'delete_task/(?P<pk>\d+)/$', views.TaskDeleteView.as_view(), name='delete_task'),
]