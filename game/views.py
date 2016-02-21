from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from game.forms import UserForm, AccountForm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost
from django.contrib.auth.models import User


# Create your views here.
@login_required()
def index(request):
    cost = Cost.objects.get(pk=1)
    acc = Account.objects.get(user=request.user)
    city = City.objects.get(account=acc)
    userlist = Account.objects.exclude(user=request.user)
    context_dict = {'userlist': userlist, 'cost': cost, 'city': city, 'acc': acc}
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
    cities = City.objects.all().filter(account=acc)
    logs = Log.objects.all().filter(city=cities).order_by('-date_occurred')[:10]
    return HttpResponse(logs)


@login_required
def battle(request, user_name):
    user = User.objects.get(username=user_name)
    account = Account.objects.get(user=user)
    city = City.objects.get(account=account)
    context_dict = {'account': account, 'city': city}
    return render(request, 'game/battle.html', context_dict)


@login_required
def alliance(request, alliance_name):
    alli = Alliance.objects.get(name=alliance_name)
    allies = Account.objects.all().filter(alliance=alli).order_by('-wins')
    owner = Account.objects.get(alliance=alli, alliance_owner=True)
    print owner
    context_dict = {'allies': allies, 'leader': owner}
    return render(request, 'game/alliance.html', context_dict)
