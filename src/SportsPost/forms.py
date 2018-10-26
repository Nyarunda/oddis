from django import forms

from .models import Question

class QuestionModelForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.TextInput (
			attrs={
			'placeholder': "Ask Sports", 
			'class': "form-control"
		
		}
             
     ))

	class Meta:
		model   = Question
		fields  = [
			# "user",
			"content"
		]