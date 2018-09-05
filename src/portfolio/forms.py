from django import forms

class contactForm(forms.Form):
	Cointegration = forms.CharField(required=True, max_length=100)
