from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
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

@login_required
def submit(request):
	if request.method == "POST":
		share_form = ShareForm(data=request.POST)
		next_url = request.POST.get("next_url", "/")
		print "submit"
		if share_form.is_valid():
			print "is_valid"
			share = share_form.save(commit=False)
			share.user = request.user
			share.save()
			return redirect(next_url)
		else:
			return newsfeed(request, share_form)
	return redirect('/')

@login_required
def newsfeed(request, share_form=None):
	share_form = share_form or ShareForm()
        shares_self = Share.objects.filter(user=user.id)
	shares_friends = Share.objects.filter(user__userprofile__in=user.profile.friends.all)
	shares = shares_self | shares_friends
	return render(request,
		'newsfeed.html',
		{'share_form': share_form, 'next_url': '/newsfeed', 
		'shares': shares, 'username': request.user.username})

def get_latest(user):
	try:
		return user.share_set.order_by('-id')[0]
	except IndexError:
		return "Index Error"

@login_required
def users(request, username="", share_form=None):
	if username:
		# show profile
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404
		shares = Share.objects.filter(user=user.id)
		if username == request.user.username or request.user.profile.friends.filter(user__username=username):
			#user's profile or his friend's profile
			return render(request, 'user.html', {'user': user, 'shares': shares, })
		return render(request, 'user.html', {'user': user, 'shares': shares, 'friends': True, })
	users = User.objects.all().annotate(share_count=Count('share'))
	shares = map(get_latest, users)
	obj = zip(users, shares)
	share_form = share_form or ShareForm()
	return render(request, 'profiles.html',
		{'obj': obj, 'next_url': '/users/', 'share_form': share_form, 'username': request.user.username, })

@login_required
def friend(request):
	if request.method == "POST":
		friend_id = request.POST.get('friend', False)
		if friend_id:
			try:
				user = User.objects.get(id=friend_id)
				request.user.profile.friends.add(user.profile)
			except ObjectDoesNotExist:
				return redirect('/users/')
	return redirect('/users/')
