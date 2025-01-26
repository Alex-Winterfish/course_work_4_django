from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import ClientModel, MessageModel

class ClientView(ListView):
    model = ClientModel

class ClientDetail(DetailView):
    model = ClientModel


class ClientCreate(CreateView):
    model = ClientModel
    fields = ["full_name", "email", "note"]
    success_url = reverse_lazy("web_mailing:clients_list")



class ClientUpdate(UpdateView):
    model = ClientModel
    fields = ["full_name", "note", "email"]
    def get_success_url(self):
        return reverse_lazy('web_mailing:client_detail', kwargs={'pk': self.object.pk})

class ClientDelite(DeleteView):
    model = ClientModel
    success_url = reverse_lazy('web_mailing:clients_list')


class MessageView(ListView):
    model = MessageModel


class MessageDetail(DetailView):
    model = MessageModel



class MessageCreate(CreateView):
    model = MessageModel
    fields = ["title", "text"]
    success_url = reverse_lazy("web_mailing:messages_list")


class MessageUpdate(UpdateView):
    model = MessageModel
    fields = ["title", "text"]
    def get_success_url(self):
        return reverse_lazy('web_mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDelete(DeleteView):
    model = MessageModel
    success_url = reverse_lazy("web_mailing:messages_list")


