from .models import Question
from .forms import QuestionModelForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Q 
from .mixins import FormUserNeededMixin, UserOwnerMixin
from django.views.generic import (
								ListView, 
								DetailView,
								DeleteView,
								CreateView, 
								UpdateView
								)
from django.contrib.auth.mixins import LoginRequiredMixin

class ReshareView(View):
	def get(self, request, pk, *args, **kwargs):
		share = get_object_or_404(Question, pk=pk)
		if request.user.is_authenticated:
			new_question = Question.objects.reshare(request.user, share)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(share.get_absolute_url())


class SportsPostCreateView(FormUserNeededMixin, CreateView):
	form_class 		= QuestionModelForm
	template_name   = "SportsPost/create_view.html"
	success_url     = "/qspost/create"


class SportsPostUpdateView(UserOwnerMixin, LoginRequiredMixin, UpdateView):
	queryset		= Question.objects.all()
	form_class 		= QuestionModelForm
	template_name   = "SportsPost/update_view.html"
	# success_url     = "/qspost/"

class SportsPostDeleteView(LoginRequiredMixin, DeleteView):
	model 			 = Question
	template_name	 = "SportsPost/delete_confirm.html"
	success_url      =  reverse_lazy("postsports:list")




class SportsPostDetailView(DetailView):
	template_name = 'SportsPost/question_detail.html'
	queryset	  = Question.objects.all()
		

class SportsPostListView(LoginRequiredMixin, ListView):
	def get_queryset(self,*args, **kwargs):
		qs	  = Question.objects.all()
		query  = self.request.GET.get("q", None)
		if query is not None:
			qs   = qs.filter(
							Q(content__icontains=query) |
							Q(user__username__icontains=query) 
						)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(SportsPostListView, self).get_context_data(*args, **kwargs)
		context['create_form']  = QuestionModelForm()
		context['create_url']   = reverse_lazy("postsports:create")
		return context 


def sport_detail_view(request, pk=None): # pk == id
    obj = get_object_or_404(Question, pk=pk)
    print(obj)
    context = {
        "object": obj
    }
    return render(request, "SportsPost/detail_view.html", context)