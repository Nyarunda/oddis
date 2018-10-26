from django.contrib import admin
from .models import Question
from .forms import QuestionModelForm


class QuestionModelAdmin(admin.ModelAdmin):
	# form     = QuestionModelForm
	class Meta:
			model 	 = Question
			
admin.site.register(Question, QuestionModelAdmin)
