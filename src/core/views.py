from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView


def index(request):
    return render(request, 'core/index.html')


class SignUpView(CreateView):
    template_name = 'core/auth/sign_up.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
