from django import forms
from clubs.models.Club import Club


class ClubForm(forms.ModelForm):
    """Formulario para editar información del Club"""

    class Meta:
        model = Club
        fields = ['president', 'email', 'phone', 'vocal_a', 'vocal_b']
        widgets = {
            'president': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nombre del presidente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'email@club.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '+593 999 999 999'
            }),
            'vocal_a': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nombre del Vocal A'
            }),
            'vocal_b': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nombre del Vocal B'
            }),
        }
        labels = {
            'president': 'Presidente',
            'email': 'Email',
            'phone': 'Teléfono',
            'vocal_a': 'Vocal A',
            'vocal_b': 'Vocal B',
        }
