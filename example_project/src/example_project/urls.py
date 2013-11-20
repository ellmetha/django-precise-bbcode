from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from test_messages.views import TestMessageCreate
from test_messages.views import TestMessageDetailView


# Admin autodiscover
admin.autodiscover()

# Patterns
urlpatterns = patterns('',
    # Admin
    url(r'^' + settings.ADMIN_URL, include(admin.site.urls)),

    # Apps
    (r'^$', TestMessageCreate.as_view()),
    url(r'^testmessage/(?P<message_pk>\d+)/$', TestMessageDetailView.as_view(), name="bbcode-message-detail"),
)

# # In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
