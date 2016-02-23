from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost
from django.contrib.auth.models import User
import datetime
from random import randint
from django.db.models import Q


# Create your views here.
@login_required()
def index(request):
    cost = Cost.objects.get(pk=1)
    acc = Account.objects.get(user=request.user)
    city = City.objects.get(account=acc)
    userlist = Account.objects.exclude(user=request.user)
    cost.wall_price = calc_wall_price(cost.wall_price, city.walls_level)
    cost.house_price = calc_house_price(cost.house_price, city.supply)
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
    acc = Account.objects.get(pk=request.user.pk)
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
    acc = Account.objects.get(pk=request.user.pk)
    alli = Alliance.objects.get(name=alliance_name)
    allies = Account.objects.all().filter(alliance=alli).order_by('-wins')
    try:
        owner = Account.objects.get(alliance=alli, alliance_owner=True)
        owner_username = owner.user.username
    except Account.DoesNotExist:
        owner_username = "N/A"
    requests = AllianceRequest.objects.filter(alliance_owner=acc)

    context_dict = {'allies': allies, 'leader': owner_username, 'acc': acc, 'requests': requests, 'alliance': alli}
    return render(request, 'game/alliance.html', context_dict)


@login_required
def alliance_request(request, alliance_name):
    acc = Account.objects.get(pk=request.user.pk)
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
    acc = Account.objects.get(pk=request.user.pk)
    if acc.alliance:
        reply = ""
        if acc.alliance_owner:
            next_in_line = \
                Account.objects.all().filter(alliance=acc.alliance).exclude(user=request.user).order_by('-wins')
            if next_in_line.count() > 0:  # appoint next in line as leader
                next_leader = next_in_line[0]
                next_leader.alliance_owner = True
                next_leader.save()
                reply = "Next in line (" + next_leader.user.username + ") now leader of alliance, "
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


@login_required
def accept_alliance(request, from_account_username):
    acc = Account.objects.get(pk=request.user.pk)
    other_user = User.objects.get(username=from_account_username)
    recruit = Account.objects.get(user=other_user)
    try:
        req = AllianceRequest.objects.get(from_account=recruit, alliance_owner=acc)
        req.delete()
        if recruit.alliance:  # check whether he is already in an alliance
            return HttpResponse(recruit.user.username + " already in an alliance!")
        else:
            recruit.alliance = acc.alliance
            recruit.save()
            return HttpResponse(recruit.user.username + " is now a member of your alliance!")
    except AllianceRequest.DoesNotExist:
        return HttpResponse("Request not found for " + recruit.user.username)


@login_required
def decline_alliance(request, from_account_username):
    acc = Account.objects.get(pk=request.user.pk)
    other_user = User.objects.get(username=from_account_username)
    recruit = Account.objects.get(user=other_user)
    try:
        req = AllianceRequest.objects.get(from_account=recruit, alliance_owner=acc)
        req.delete()
        return HttpResponse("You declined " + recruit.user.username + " from becoming a member of your alliance!")
    except AllianceRequest.DoesNotExist:
        return HttpResponse("Request not found for " + recruit.user.username)


@login_required
def get_gold(request):
    acc = Account.objects.get(pk=request.user.pk)
    city = City.objects.all().get(account=acc)
    return HttpResponse(city.gold)


@login_required
def buy(request):
    if request.method == 'GET':
        element_type = request.GET['element_type']
    else:
        return HttpResponse("-2")

    acc = Account.objects.get(pk=request.user.pk)
    city = City.objects.all().get(account=acc)
    cost = Cost.objects.all().get()

    if element_type == 'supply':
        temp_cost = calc_house_price(cost.house_price, city.supply)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.supply += 50
            city.save()
            return HttpResponse(str(city.supply) + "," + str(calc_house_price(cost.house_price, city.supply)))
    if element_type == 'wall':
        temp_cost = calc_wall_price(cost.wall_price, city.walls_level)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.walls_level += 1
            city.save()
            return HttpResponse(str(city.walls_level) + "," + str(calc_wall_price(cost.wall_price, city.walls_level)))
    if city.footmen+city.bowmen+city.knights+city.war_machines<city.supply:
    	if element_type == 'footmen':
        	if city.gold >= 10:
        		city.gold -= 10
            	city.footmen += 1
            	city.save()
            	return HttpResponse(city.footmen)
    	if element_type == 'bowmen':
        	if city.gold >= 15:
        	    city.gold -= 15
            	city.bowmen += 1
            	city.save()
            	return HttpResponse(city.bowmen)
   		if element_type == 'knights':
   			if city.gold >= 25:
   				city.gold -= 25
            	city.knights += 1
            	city.save()
            	return HttpResponse(city.knights)
    	if element_type == 'war_machines':
        	if city.gold >= 50:
        		city.gold -= 50
            	city.war_machines += 1
            	city.save()
            	return HttpResponse(city.war_machines)
    	return HttpResponse("-1")

def calc_house_price(base, supply):
    return base + supply


def calc_wall_price(base, level):
    return base * (level + 1)


@login_required
def attack(request, opponent):
    user = User.objects.get(username=opponent)
    enemyaccount = Account.objects.get(user=user)
    ecity = City.objects.all().get(account=enemyaccount)
    acc = Account.objects.get(pk=request.user.pk)
    city = City.objects.all().get(account=acc)
    
    if city.footmen + (city.bowmen * 1.5) + (city.knights * 2) + (city.war_machines * 4) > (
                ecity.footmen + (ecity.bowmen * 1.5) + (ecity.knights * 2) + (ecity.war_machines * 4)) * (
        (10 + ecity.walls_level) / 10):
        rnggold = randint(10, 15)
        tempgold = ecity.gold / rnggold
        loseArmy(city, ecity, False, True, user, tempgold)
        loseArmy(ecity, city, True, False, request.user, tempgold)
        print "victory"
        return HttpResponse("victory")
    else:
        rnggold = randint(5, 10)
        tempgold = city.gold / rnggold
        loseArmy(city, ecity, False, False, user, tempgold)
        loseArmy(ecity, city, True, True, request.user, tempgold)
        print "defeat"
        return HttpResponse("defeat")


def loseArmy(city, ecity, defender, winner, user, tempgold):
    if defender:
        if winner:
            rng = randint(5, 15)
            city.gold += tempgold
            ecity.gold -= tempgold
            createWinLog(city, user, rng, defender, tempgold)
        else:
        	rng = randint(15, 30)
        	createDefeatLog(city, user, rng, defender, tempgold)
        	city.gold -= tempgold
        	ecity.gold += tempgold
    else:
        if winner:
            rng = randint(15, 30)
            createWinLog(city, user, rng, defender, tempgold)
            city.gold += tempgold
            ecity.gold -= tempgold
        else:
        	rng = randint(30, 50)
        	createDefeatLog(city, user, rng, defender, tempgold)
        	city.gold -= tempgold
        	ecity.gold += tempgold

    city.footmen -= city.footmen * rng / 100
    city.bowmen -= city.bowmen * rng / 100
    city.knights -= city.knights * rng / 100
    city.war_machines -= city.war_machines * rng / 100

    ecity.save()
    city.save()


def createWinLog(city, user, casualties, defender, tempgold):
    if defender:
        log = Log.objects.create(city=city,
                                 text="you defended your city successfully from " + user.username + " losing " + str(
                                     casualties) + " % of your troops and gaining " + str(
                                     tempgold) + " gold coins from your enemy")
    else:
        log = Log.objects.create(city=city, text="you defeated " + user.username + " losing " + str(
            casualties) + " % of your troops and gaining " + str(tempgold) + " gold coins from your enemy")
    log.save()


def createDefeatLog(city, user, casualties, defender, tempgold):
    if defender:
        log = Log.objects.create(city=city,
                                 text="you failed to defend your city from " + user.username + " losing " + str(
                                     casualties) + " % of your troops and " + str(tempgold) + " gold coins")
    else:
        log = Log.objects.create(city=city, text="you suffered a defeat from " + user.username + " losing " + str(
            casualties) + " % of your troops and " + str(tempgold) + " gold coins")
    log.save()


@login_required
def create_alliance(request):
    if request.method == 'GET':
        name = request.GET['name']
        desc = request.GET['desc']
    else:
        # missing data exit
        return HttpResponse("-2")

    acc = Account.objects.get(pk=request.user.pk)
    try:
        # create alliance
        created_alliance = Alliance.objects.create(name=name, description=desc)
        created_alliance.save()
    except Alliance.IntegrityError:
        return HttpResponse("Name Exists")
    # alliance successfully created
    acc.alliance = created_alliance
    acc.alliance_owner = True
    return HttpResponse("1")


@login_required
def alliance_search(request, query):
    similar_alliances = Alliance.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context_dict = {'similar_alliances': similar_alliances, 'query': query}
    return render(request, 'game/alliance_search.html', context_dict)
