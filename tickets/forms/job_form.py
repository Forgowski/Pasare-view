from datetime import date
from django import forms


class TooltipInputFactory:
    def __call__(self, base_widget=forms.TextInput, tooltip_text='', *args, **kwargs):
        class TooltipTextInput(base_widget):
            def __init__(self, tooltip_text=None, *args, **kwargs):
                self.tooltip_text = tooltip_text
                super().__init__(*args, **kwargs)

            def is_hidden(self):
                return False

            def render(self, name, value, attrs=None, renderer=None):
                html = super().render(name, value, attrs, renderer)
                tooltip_html = (
                    f'<a href="#" title="{self.tooltip_text}">'
                    '<img src="https://shots.jotform.com/kade/Screenshots/blue_question_mark.png" height="13px"/>'
                    '</a>'
                )
                return f'{tooltip_html} {html}'

        return TooltipTextInput(tooltip_text=tooltip_text, *args, **kwargs)


TooltipFactory = TooltipInputFactory()


class JobForm(forms.Form):
    LUGGAGE_OPTIONS = [
        ('Podręczny', 'Podręczny (darmowy)'),
        ('Rejestrowany', 'Rejestrowany'),
        ('dodatkowy bagaż podręczny', 'dodatkowy bagaż podręczny')
    ]
    FLY_OPTIONS = [
        ('Klasa ekonomiczna', 'Klasa ekonomiczna'),
        ('Klasa premium', 'Klasa premium'),
        ('Biznes klasa', 'Biznes klasa'),
        ('Pierwsza klasa', 'Pierwsza klasa'),
    ]
    TRIP_OPTIONS = [
        ('W jedną stronę', 'W jedną stronę'),
        ('W dwie strony', 'W dwie strony'),
        ('Wiele miast', 'Wiele miast'),
    ]
    TRIP_TARGET_OPTIONS = [
        ('Europa', 'Europa (10zł)'),
        ('Interkontynentalny', 'Interkontynentalny (20zł)'),
    ]
    trip_target = forms.ChoiceField(
        choices=TRIP_TARGET_OPTIONS,
        widget=forms.RadioSelect,
        label="Lot",
        initial="Europa"
    )
    your_name = forms.CharField(label="Imię",
                                max_length=100)

    whatsapp = forms.CharField(label="Nr telefonu WhatsApp (opcjonalnie)", required=False, max_length=100)

    email = forms.CharField(label="Email kontaktowy", max_length=100)

    trip_option = forms.ChoiceField(
        choices=TRIP_OPTIONS,
        widget=forms.RadioSelect,
        label="W jedną czy dwie strony?"
    )

    city = forms.CharField(label="Z (miasto)", max_length=100, widget=TooltipFactory(
        tooltip_text="Czasami bilety lotnicze z pobliskich miast są nawet kilkukrotnie tańsze w porównaniu z wybranym"
                     " przez Ciebie lotnisku. Jeżeli chcesz abyśmy dla Ciebie porównali ceny z innymi miastami wypisz je"
                     " w polu przeznaczonym na dodatkowe informację. Możesz podać miasta a nawet sąsiednie kraje lub"
                     " zasięg kilometrowy od Twojego miasta."
                     ""))

    target_city = forms.CharField(label="Do (miasto)", max_length=100,
                                  widget=TooltipFactory(
                                      tooltip_text="Czasami bilety lotnicze do pobliskich miast są nawet kilkukrotnie"
                                                   " tańsze w porównaniu z wybranym przez Ciebie lotnisku. Jeżeli chcesz"
                                                   " abyśmy dla Ciebie porównali ceny z innymi miastami wypisz je"
                                                   " w polu przeznaczonym na dodatkowe informację. Możesz podać miasta a"
                                                   " nawet sąsiednie kraje lub zasięg kilometrowy od Twojego miasta."
                                  ))

    cities = forms.CharField(label='',
                             widget=forms.TextInput(attrs={'class': 'hidden', 'placeholder': "Podaj pozostałe miasta"}),
                             required=False)

    number_of_people = forms.IntegerField(label="Liczba osób", min_value=1,
                                          widget=TooltipFactory(forms.NumberInput,
                                                                tooltip_text="Podaj łączną liczbę osób (procent pobierany od ceny biletu za wykonaną usługę dotyczy tylko równowartości biletu dla 1 osoby)"
                                                                ))

    out_date = forms.DateField(
        label="Data wylotu",
        widget=TooltipFactory(forms.DateInput,
                              tooltip_text="Czasami bilety lotnicze w innych datach (nawet dzień różnicy)"
                                           " są nawet kilkukrotnie tańsze w porównaniu z wybranym przez"
                                           " Ciebie datami. Jeżeli chcesz abyśmy dla Ciebie porównali"
                                           " ceny w innych datach wypisz je w polu przeznaczonym na dodatkowe"
                                           " informację. Możesz podać inne, konkretne daty lub"
                                           " przedział dat a nawet zaznaczyć cały, interesujący"
                                           " Cię miesiąc.",
                              attrs={'type': 'date', 'min': str(date.today())})
    )

    back_date = forms.DateField(
        label="Data powrotu",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )

    luggage = forms.ChoiceField(
        choices=LUGGAGE_OPTIONS,
        widget=forms.RadioSelect,
        label="Jaki rodzaj bagażu"
    )

    fly_class = forms.ChoiceField(
        choices=FLY_OPTIONS,
        widget=forms.RadioSelect,
        label="Wybierz klasę lotu"
    )

    max_price = forms.CharField(label="Maksymalna cena biletu", max_length=100,
                                widget=TooltipFactory(tooltip_text="Maksymalna cena za bilet dla jednej osoby w jedną"
                                                                   " lub dwie strony (zależnie od wybranej oferty),"
                                                                   " nie wliczając ceny wykonania usługi (która wynosi 10%)"
                                                      ))

    number_of_offers = forms.IntegerField(label="Liczba ofert (każda powyżej 2 dodatkowe 10zł)", min_value=2, initial=2,
                                          widget=forms.NumberInput)

    additional_information = forms.CharField(
        label="Dodatkowe informacje",
        widget=forms.Textarea(),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        out_date = cleaned_data.get('out_date')
        back_date = cleaned_data.get('back_date')

        if out_date and back_date and back_date < out_date:
            self.add_error('back_date', "Data powrotu nie może być wcześniejsza niż data wylotu.")
