from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    ### Browsing ###
    url(r'^$', 'bookmarks.views.main'),
    url(r'^user/(\w+)/$', 'bookmarks.views.user_page'),
    url(r'^tag/([^\s]+)/$','bookmarks.views.tag_page'),
    url(r'^tag/$', 'bookmarks.views.tag_cloud'),

    ### Account Management ###
    url(r'^save/$', 'bookmarks.views.bookmark_save'),


    ### Session Management###
    #url(r'^login/$', 'bookmarks.views.login'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
#    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'bookmarks.views.logout_view'),
    url(r'^change-password/$', 'django.contrib.auth.views.password_change'),
    url(r'^password-changed/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^register/$', 'bookmarks.views.register_page'),
    url(r'^register/success/$', TemplateView.as_view(template_name='registration/register_success.html')),
)

#urlpatterns += staticfiles_urlpatterns()