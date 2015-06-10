from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings 
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
from usermanager import views
from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include("usermanager.urls",namespace='usermanager', app_name='usermanager')),
    
    

    url(r'^static/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),
    url(r'^home',views.setting),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
