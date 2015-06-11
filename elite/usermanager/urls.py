from django.conf.urls import patterns, url
from usermanager import views
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
                        url(r'^setting/$', views.setting,name="setting"),
                        url(r'^setting/(?P<pk>[\d]+)/$', views.result,name='result'),

)
