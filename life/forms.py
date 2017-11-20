from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)
    email = forms.CharField()
    def pwd_validate(self,p1,p2):
	return p1==p2
