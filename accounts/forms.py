from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="ID",
        widget=forms.TextInput(attrs={
            "placeholder": "사용하실 ID를 입력해주세요",
        })
    )
    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호를 8자리 이상 입력해주세요.",
        })
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호를 다시 한번 입력해주세요.",
        })
    )
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2',)

