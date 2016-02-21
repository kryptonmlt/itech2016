from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost
from django.contrib.auth.models import User
import datetime


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
    acc = Account.objects.get(pk=request.user.pk);
    alli = Alliance.objects.get(name=alliance_name)
    allies = Account.objects.all().filter(alliance=alli).order_by('-wins')
    owner = Account.objects.get(alliance=alli, alliance_owner=True)
    context_dict = {'allies': allies, 'leader': owner, 'acc': acc}
    return render(request, 'game/alliance.html', context_dict)


@login_required
def alliance_request(request, alliance_name):
    acc = Account.objects.get(pk=request.user.pk);
    if acc.alliance:
        return HttpResponse("Leave alliance first!")

    alli = Alliance.objects.get(name=alliance_name)
    owner = Account.objects.get(alliance=alli, alliance_owner=True)

    already_exists = AllianceRequest.objects.filter(from_account=acc, alliance_owner=owner)
    if already_exists:
        return HttpResponse("Already submitted")
    else:
        msg = None
        if request.method == 'GET':
            msg = request.GET['msg']
        print str(datetime.datetime.now)
        all_req = AllianceRequest.objects.create(from_account=acc, alliance_owner=owner, text=msg)
        all_req.save()
        return HttpResponse("Submitted")


@login_required
def leave_alliance(request):
    acc = Account.objects.get(pk=request.user.pk);
    if acc.alliance:
        reply=""
        if acc.alliance_owner:
            next_in_line = \
                Account.objects.all().filter(alliance=acc.alliance).exclude(user=request.user).order_by('-wins')
            if next_in_line.count() > 0:  # appoint next in line as king
                next_leader = next_in_line[0]
                next_leader.alliance_owner = True
                next_leader.save()
                reply = "Next in line ("+next_leader.user.username+") now leader of alliance, "
            else:  # delete alliance since no one left to take it
                acc.alliance.delete()
                reply = "No one next in line, alliance collapsed, "
        acc.alliance = None
        acc.alliance_owner = False
        acc.save()
        reply += "Alliance Left successfully"
    else:
        reply = "Not in an alliance"

    return HttpResponse(reply)
