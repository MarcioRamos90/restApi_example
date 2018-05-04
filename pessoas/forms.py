from django import forms

from .models import Pessoa


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = [
            'first_name',
            'last_name',
            'picture'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if first_name is None or last_name is None:
            raise forms.ValidationError("error: First name and last name are required")
        return super().clean(*args, **kwargs)