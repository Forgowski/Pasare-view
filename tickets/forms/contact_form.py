from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Imię")
    email = forms.CharField(max_length=100, label="Email kontaktowy")
    whatsapp = forms.CharField(max_length=100, label="Nr kontaktowy WhatsApp (opcjonalnie)", required=False)
    message = forms.CharField(
        label="Treść wiadomości",
        widget=forms.Textarea())

