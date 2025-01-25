from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, TemplateView, UpdateView, DeleteView
from .models import ClientModel, MessageModel

class ClientView(ListView):
    model = ClientModel

class ClientDetail(DetailView):
    model = ClientModel
    pass

class ClientCreate(CreateView):
    model = ClientModel
    fields = ["full_name", "email", "note"]
    success_url = reverse_lazy("web_mail:")
    pass
class ClientUpdate(UpdateView):
    model = ClientModel
    pass



