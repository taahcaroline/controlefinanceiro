from django import forms
from .models import Movimentacao, Categoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model



Usuario = get_user_model()


class CadastroUsuarioForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        })
    )

class ReceitaForm(forms.ModelForm):

    class Meta:
        model = Movimentacao

        fields = [
            'descricao',
            'categoria',
            'valor',
            'data',
            'forma_pagamento',
            'observacao',
        ]

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Salário de novembro / Serviço X de freelancer'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),

            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01'
            }),

            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'forma_pagamento': forms.Select(attrs={
                'class': 'form-control'
            }),

            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')

        super().__init__(*args, **kwargs)

        self.fields['categoria'].queryset = Categoria.objects.filter(
            usuario=usuario,
            tipo='R'
        )

class DespesaForm(forms.ModelForm):

    class Meta:
        model = Movimentacao

        fields = [
            'descricao',
            'categoria',
            'valor',
            'data',
            'forma_pagamento',
            'observacao',
        ]

        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Aluguel'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),

            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'step': '0.01'
            }),

            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'forma_pagamento': forms.Select(attrs={
                'class': 'form-control'
            }),

            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')

        super().__init__(*args, **kwargs)

        self.fields['categoria'].queryset = Categoria.objects.filter(
            usuario=usuario,
            tipo='D'
        )


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = ['nome', 'tipo']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Salário / Água / Lazer / Luz'
            }),

            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
        }