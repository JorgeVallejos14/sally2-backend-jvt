from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nombre', 'email', 'cantidad']
        labels = {
            'nombre': 'Tu nombre',
            'email': 'Tu correo',
            'cantidad': 'Cantidad de entradas',
        }
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 1 or cantidad > 10:
            raise forms.ValidationError("La cantidad debe estar entre 1 y 10.")
        return cantidad