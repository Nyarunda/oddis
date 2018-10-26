from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	email    = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Password must match")
		return password2


	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__icontains=username).exists():
			raise forms.ValidationError("This username is  taken")
		return username


	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__icontains=email).exists():
			raise forms.ValidationError("This email is already registered")
		return email