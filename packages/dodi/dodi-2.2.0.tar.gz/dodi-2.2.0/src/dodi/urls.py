from django.urls import re_path
from ._views import ImageResponder

urlpatterns = [
    re_path(r'^(?P<transform>.*)$', ImageResponder.handle, name='dodi_image')
]