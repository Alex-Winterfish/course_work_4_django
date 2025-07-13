from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import ClientModel, MessageModel, MailingModel, MailingAttemptModel
from .forms import StyleFormMixin, MailingForm, MailingAttemptForm
from dotenv import load_dotenv
from .services import start_mailing

load_dotenv()


@method_decorator(cache_page(60 * 1), name="dispatch")
class ClientView(LoginRequiredMixin, ListView):
    model = ClientModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name="managers").exists():
            return ClientModel.objects.filter(owner=user)
        elif user.groups.filter(name="managers").exists():
            return ClientModel.objects.all()
        return super().get_queryset()

    login_url = reverse_lazy("web_mailing:main")


class ClientDetail(DetailView):
    model = ClientModel


class ClientCreate(StyleFormMixin, CreateView):
    model = ClientModel
    fields = ["full_name", "email", "note"]
    success_url = reverse_lazy("web_mailing:clients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class ClientUpdate(StyleFormMixin, UpdateView):
    model = ClientModel
    fields = ["full_name", "note", "email"]

    def get_success_url(self):
        return reverse_lazy("web_mailing:client_detail", kwargs={"pk": self.object.pk})


class ClientDelite(DeleteView):
    model = ClientModel
    success_url = reverse_lazy("web_mailing:clients_list")


@method_decorator(cache_page(60 * 1), name="dispatch")
class MessageView(LoginRequiredMixin, ListView):
    model = MessageModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name="managers").exists():
            return MessageModel.objects.filter(owner=user)
        elif user.groups.filter(name="managers").exists():
            return MessageModel.objects.all()
        return super().get_queryset()

    login_url = reverse_lazy("web_mailing:main")


class MessageDetail(DetailView):
    model = MessageModel


class MessageCreate(StyleFormMixin, CreateView):
    model = MessageModel
    fields = ["title", "text"]

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)

    success_url = reverse_lazy("web_mailing:messages_list")


class MessageUpdate(StyleFormMixin, UpdateView):
    model = MessageModel
    fields = ["title", "text"]

    def get_success_url(self):
        return reverse_lazy("web_mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageDelete(DeleteView):
    model = MessageModel
    success_url = reverse_lazy("web_mailing:messages_list")


@method_decorator(cache_page(60 * 1), name="dispatch")
class MailingView(LoginRequiredMixin, ListView):
    model = MailingModel

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name="managers").exists():
            return MailingModel.objects.filter(owner=user)
        elif user.groups.filter(name="managers").exists():
            return MailingModel.objects.all()
        return super().get_queryset()

    login_url = reverse_lazy("web_mailing:main")


class MailingUpdate(StyleFormMixin, UpdateView):
    model = MailingModel
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("web_mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingCreate(StyleFormMixin, CreateView):
    model = MailingModel
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("web_mailing:mailing_list")


class MailingDetail(DetailView):
    model = MailingModel


class MailingDelete(DeleteView):
    model = MailingModel
    success_url = reverse_lazy("web_mailing:mailing_list")


class MailingAttemptView(LoginRequiredMixin, ListView):
    model = MailingAttemptModel

    def get_queryset(self):
        user = self.request.user
        if (
            user.is_authenticated
        ):  # получаем попытки рассылок для зарегистрированного пользователя
            return MailingAttemptModel.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        user = self.request.user
        mailing_done = MailingModel.objects.filter(
            owner=user, status="Окончена"
        )  # получаем оконченные рассылки
        messages = 0  # переменная для накопления числа сообщений
        for (
            mailing
        ) in mailing_done:  # цикл для подсчета сообщений, отправленных клиентам
            messages += mailing.recipients.count()
        success_attempt = 0
        fail_attempt = 0
        attempts = self.get_queryset()
        for attempt in attempts:
            if attempt.status == "Успешно":
                success_attempt += 1
            else:
                fail_attempt += 1
        context = super().get_context_data(**kwargs)
        context["success_attempt"] = success_attempt
        context["fail_attempt"] = fail_attempt
        context["messages"] = messages

        return context

    login_url = reverse_lazy("web_mailing:main")


class MailingAttemptCreate(StyleFormMixin, CreateView):
    model = MailingAttemptModel
    form_class = MailingAttemptForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя
        return kwargs

    def form_valid(self, form):

        start_mailing(self, form)

        return super().form_valid(form)

    success_url = reverse_lazy("web_mailing:mailing_attempt")


@method_decorator(cache_page(60 * 1), name="dispatch")
class MainPageView(TemplateView):
    template_name = "web_mailing/main.html"

    mailing_count = MailingModel.objects.count()
    mailing_active = MailingModel.objects.filter(status="Начата").count()
    clients = ClientModel.objects.all()

    emails = set()
    for client in clients:
        emails.add(client.email)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["mailing_count"] = self.mailing_count
        context["mailing_active"] = self.mailing_active
        context["clients"] = len(self.emails)

        return context


def end_mailing(request, pk):
    """Функция для отключения рассылки"""
    mailing = MailingModel.objects.get(id=pk)
    if mailing.status in ["Окончена"]:
        mailing.status = "Начата"
        mailing.save()
    else:
        mailing.status = "Окончена"
        mailing.save()

    return redirect(f"/web_mailing/mailing_detail/{pk}")
