from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from test_messages.views import TestMessageCreate
from test_messages.views import TestMessageDetailView


# Admin autodiscover
admin.autodiscover()

# Patterns
urlpatterns = [
    # Admin
    url(r'^' + settings.ADMIN_URL, admin.site.urls),

    # Apps
    url(r'^$', TestMessageCreate.as_view()),
    url(r'^testmessage/(?P<message_pk>\d+)/$', TestMessageDetailView.as_view(), name="bbcode-message-detail"),
]

# # In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += [
        url(r'^%s/(?P<path>.*)$' % media_url, serve, {'document_root': settings.MEDIA_ROOT}),
    ]
