from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.db.models import Q 
from django.views import View
from django.views.generic import ListView

from SportsPost.models import Question
# from SportsPost.views import SportsPostListView
User = get_user_model()

from .forms import ContactForm, LoginForm, RegisteraForm

def home(request):
	context = {
		"title": "Hello, world!, Welcome to SportyPoint",
		"content": "This is your home"

	}
	if request.user.is_authenticated:
		context["premium_content"] = "Yeahhhhhh"

	return render(request, "home.html", context)

class SearchView(View):
	def get(self, request, *args, **kwargs):
		query = request.GET.get("q")
		qs = None
		if query:
			qs = User.objects.filter(
				Q(username__icontains=query)
			)
		context = {"users": qs}
		return render(request, 'search.html', context)


class SportsPostListView(ListView):
	template_name = "home.html"
	queryset	  = Question.objects.all()


def trending(request):
	context = {
		"title": "Hello, world!, Our Latest Trending",
		"content": "This is your home"
	}
	return render(request, "trending_view.html", context)

# def is_authenticated(user):
#     if callable(user.is_authenticated):
#         return user.is_authenticated()
#     return user.is_authenticated

def login_page(request):
	form = LoginForm(request.POST or None)
	context ={
		"form": form
	}
	print("User logined in")
	# print(request.user.is_authenticated)
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username=username, password=password)
		# print(request.user.is_authenticated)
		if user is not None:
			# print(request.user.is_authenticated)
			login(request, user)
			# context["form"] = LoginForm()
			return redirect("/login")
		else:
			print("Error")
	return render(request, "auth/login_view.html", context)

def register_page(request):
	form = RegisteraForm(request.POST or None)
	context ={
		"form": form
	}
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email    = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)
	return render(request, "auth/register_view.html", context)


def odds(request):
	context = {
		"title": "Hello, world!, Our Latest Free Odds",
		"content": "This is your home"
	}
	return render(request, "odds_view.html", context)

def contact(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title": "Hello, world!, Contact Me Here",
		"content": "This is your home",
		"form": contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
	return render(request, "contact/view.html", context)