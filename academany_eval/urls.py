"""academany_eval URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django_markdown import flatpages
from django.contrib.sites.models import Site
from courses.admin import admin_site
import dashboard
import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

# some customization to the admin changing titles and adding flatpages


# flatpages.register()

admin_site.register(FlatPage,FlatPageAdmin)

urlpatterns = [
    url(r'^api/', include('courses.urls')),
    url(r'^markdown/', include( 'django_markdown.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin_site.urls),
    url(r'^login/$', auth_views.login,  name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^$', auth_views.login)
] 
