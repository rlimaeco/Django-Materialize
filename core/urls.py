from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

from core import views as core_views


urlpatterns = [
    url(r'^$', core_views.index, name='index'),
    url(r'^signup/', core_views.SignUpView.as_view(), name='sign_up'),
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
