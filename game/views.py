from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from game.forms import UserForm, AccountForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost


# Create your views here.
@login_required()
def index(request):
	cost=Cost.objects.get(pk=1)
	acc=Account.objects.get(user=request.user)
	city=City.objects.get(account=acc)
	userlist = Account.objects.exclude(user=request.user)
	context_dict = {'userlist': userlist,'cost':cost,'city':city}
	print "game page loaded!"
	return render(request, 'game/game.html', context_dict)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

@login_required
def get_logs(request):
    acc = Account.objects.get(pk=request.user.pk);
    cities = City.objects.get(account=acc)
    logs = Log.objects.objects(city=cities).orderby('-date_occurred')
    return HttpResponse(logs)