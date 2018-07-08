"""TwitterProject URL Configuration

"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from apptwitter.views import addMessage, userPage

urlpatterns = [

    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('allauth.urls')),
    path('', addMessage),
    path('auth', TemplateView.as_view(template_name='user/auth.html')),
    re_path(r'^accounts/profile/$', TemplateView.as_view(template_name='user/profile.html')),
    re_path('^user/(?P<userid>\w+)/$', userPage),

]
