from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from fbclone_app.forms import AuthenticateForm, UserCreateForm, ShareForm
from fbclone_app.models import Share

def index(request, auth_form=None, user_form=None):
	#user is logged in
	if request.user.is_authenticated():
		share_form = ShareForm()
		user = request.user
		shares_self = Share.objects.filter(user=user.id)
		shares_friends = Share.objects.filter(user__userprofile__in=user.profile.friends.all)
		shares = shares_self | shares_friends

		return render(request,
			'friends.html',
			{'share_form': share_form, 'user': user,
			'shares': shares,
			'next_url':'/', })

	else:
		#user is not logged in
		auth_form = auth_form or AuthenticateForm()
		user_form = user_form or UserCreateForm()

		return render(request,
			'home.html',
			{'auth_form': auth_form, 'user_form':user_form, })

# Create your views here.

def login_view(request):
	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			# success!
			return redirect('/')
		else:
			# failure
			return index(request, auth_form=form)
	return redirect('/')

def logout_view(request):
	logout(request)
	return redirect('/')

def signup(request):
	user_form = UserCreateForm(data=request.POST)
	if request.method == 'POST':
		if user_form.is_valid():
			username = user_form.clean_username()
			password = user_form.clean_password2()
			user_form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('/')
		else:
			return index(request, user_form=user_form)
	return redirect('/')