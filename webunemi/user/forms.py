from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)
    city = forms.CharField(label='Ciudad', max_length=50)
    phone_number = forms.CharField(label='Número de teléfono', max_length=15)
    address = forms.CharField(label='Dirección', max_length=255)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'phone_number', 'username', 'password1', 'password2', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('city'),
            Field('phone_number'),
            Field('username'),
            Field('password1'),
            Field('password2'),
            Field('address'),
            Submit('register', 'Registrar')
        )

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            Submit('login', 'Iniciar sesión')
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'phone_number', 'username', 'address', 'profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 mt-1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['first_name', 'last_name', 'email', 'city', 'phone_number', 'username', 'address']:
            self.fields[field].disabled = True
        self.fields['profile_image'].required = False