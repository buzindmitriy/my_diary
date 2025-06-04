from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "pages/home.html"

def custom_permission_denied(request, exception=None):
    return render(request, '403.html', status=403)