from django.forms import BooleanField, ModelForm
from web_mailing.models import MailingModel, MessageModel,ClientModel

class StyleFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
        return form


class MailingForm(ModelForm):
    class Meta:
        model = MailingModel
        fields = ["message", "recipients"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = MessageModel.objects.filter(owner=user)
        self.fields['recipients'].queryset = ClientModel.objects.filter(owner=user)