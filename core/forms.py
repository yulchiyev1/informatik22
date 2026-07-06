from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, StudentPost


class RegisterForm(UserCreationForm):
    """
    Registration form extending Django's built-in UserCreationForm.
    All labels are in Uzbek for the UI.
    """
    username = forms.CharField(
        max_length=150,
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Foydalanuvchi nomingizni kiriting"
        })
    )
    password1 = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Parolingizni kiriting"
        })
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Parolni qayta kiriting"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    """
    Simple login form with Uzbek labels.
    """
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Foydalanuvchi nomingizni kiriting"
        })
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Parolingizni kiriting"
        })
    )


class ProfileForm(forms.ModelForm):
    """
    Form allowing users to update their full name and class.
    """
    full_name = forms.CharField(
        max_length=150,
        required=False,
        label="To'liq ism",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ismingizni kiriting"
        })
    )
    student_class = forms.CharField(
        max_length=50,
        required=False,
        label="Sinfingiz",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Masalan: 10-A"
        })
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'student_class']


class StudentPostForm(forms.ModelForm):
    """
    Form for students to create a learning post.
    """
    title = forms.CharField(
        max_length=200,
        label="Sarlavha",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Postingiz sarlavhasini kiriting"
        })
    )
    photo = forms.ImageField(
        required=False,
        label="Rasm (ixtiyoriy)",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )
    learned_today = forms.CharField(
        label="Bugun nimani o'rgandim?",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': "Bugun o'rgangan narsalaringizni yozing..."
        })
    )
    experience = forms.CharField(
        label="Tajribam",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': "Qanday qiyinchiliklar va yutuqlarga duch keldingiz?"
        })
    )

    class Meta:
        model = StudentPost
        fields = ['title', 'photo', 'learned_today', 'experience']
