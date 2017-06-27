from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(
        r'^login/',
        auth_views.login,
        {"template_name": "core/auth/login.html"},
        name='login'),
    url(
        r'^logout/',
        auth_views.logout,
        {'next_page': reverse_lazy('login')},
        name='logout'),
]
