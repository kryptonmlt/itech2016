from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost, CityGraphic
from django.contrib.auth.models import User
from game.forms import CityForm
import datetime
from random import randint
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
@login_required()
def index(request):
    cost = Cost.objects.get(pk=1)
    acc = Account.objects.get(user=request.user)
    try:
        city = City.objects.get(account=acc)
    except City.DoesNotExist:
        city = None
        err_msg = ""
        if request.method == 'POST':
            city_form = CityForm(data=request.POST)
            if city_form.is_valid():
                city = city_form.save(commit=False)
                city.account = acc
                city.save()
            else:
                err_msg = "Form was not valid!"
        if city is None:
            city_form = CityForm()
            return render(request, 'game/create_city.html', {'city_form': city_form, 'acc': acc, 'err_msg': err_msg})

    userlist = Account.objects.exclude(user=request.user)
    cost.wall_price = calc_wall_price(cost.wall_price, city.walls_level)
    cost.house_price = calc_house_price(cost.house_price, city.house_level)
    cost.lands_price = calc_lands_price(cost.lands_price, city.lands_owned)
    city_pic = CityGraphic.objects.get(level=get_correct_image(city.house_level))
    context_dict = {'userlist': userlist, 'cost': cost, 'city': city, 'acc': acc, 'city_pic': city_pic}
    return render(request, 'game/game.html', context_dict)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


@login_required
def get_logs(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    cities = City.objects.all().filter(account=acc)
    try:
        last_log_id = request.GET['latest_log_id']
        if last_log_id == -1:
            logs = Log.objects.all().filter(city=cities).order_by('date_occurred')[:10]
        else:
            logs = Log.objects.all().filter(city=cities, pk__gt=last_log_id).order_by('date_occurred')
    except MultiValueDictKeyError:
        logs = Log.objects.all().filter(city=cities).order_by('date_occurred')[:10]
    return HttpResponse(logs)


@login_required
def battle(request, user_name):
    user = User.objects.get(pk=request.user.pk)
    account = Account.objects.get(user=user)
    enemy_user = User.objects.get(username=user_name)
    enemy_account = Account.objects.get(user=enemy_user)
    enemy_city = City.objects.get(account=enemy_account)
    city = City.objects.get(account=account)
    context_dict = {'enemy_city': enemy_city, 'city': city}
    return render(request, 'game/battle.html', context_dict)


@login_required
def alliance(request, alliance_name):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    alli = Alliance.objects.get(name=alliance_name)
    allies = Account.objects.all().filter(alliance=alli).order_by('-wins')
    owner = False
    try:
        owner = Account.objects.get(alliance=alli, alliance_owner=True)
        owner_username = owner.user.username
        if owner_username == acc.user.username:
            owner = True
    except Account.DoesNotExist:
        owner_username = "N/A"
    if owner:
        requests = AllianceRequest.objects.filter(alliance=alli)
    else:
        requests = ""

    context_dict = {'allies': allies, 'leader': owner_username, 'acc': acc, 'requests': requests, 'alliance': alli}
    return render(request, 'game/alliance.html', context_dict)


@login_required
def alliance_request(request, alliance_name):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    if acc.alliance:
        if acc.alliance.name == alliance_name:
            return HttpResponse("You are already in this alliance!")
        else:
            return HttpResponse("Leave alliance first!")

    alli = Alliance.objects.get(name=alliance_name)

    already_exists = AllianceRequest.objects.filter(from_account=acc, alliance=alli)
    if already_exists:
        return HttpResponse("Already submitted")
    else:
        msg = None
        if request.method == 'GET':
            msg = request.GET['msg']
        print str(datetime.datetime.now)
        all_req = AllianceRequest.objects.create(from_account=acc, alliance=alli, text=msg)
        all_req.save()
        return HttpResponse("Submitted")


@login_required
def leave_alliance(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
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
    user = User.objects.get(pk=request.user.pk)
    leader = Account.objects.get(user=user)
    other_user = User.objects.get(username=from_account_username)
    recruit = Account.objects.get(user=other_user)
    try:
        req = AllianceRequest.objects.get(from_account=recruit, alliance=leader.alliance)
        req.delete()
        if recruit.alliance:  # check whether he is already in an alliance
            return HttpResponse(recruit.user.username + " is already in an alliance!")
        else:
            recruit.alliance = leader.alliance
            recruit.save()
            return HttpResponse(recruit.user.username + " is now a member of your alliance!")
    except AllianceRequest.DoesNotExist:
        return HttpResponse("Request not found for " + recruit.user.username)


@login_required
def decline_alliance(request, from_account_username):
    user = User.objects.get(pk=request.user.pk)
    leader = Account.objects.get(user=user)
    other_user = User.objects.get(username=from_account_username)
    recruit = Account.objects.get(user=other_user)
    try:
        req = AllianceRequest.objects.get(from_account=recruit, alliance=leader.alliance)
        req.delete()
        return HttpResponse("You declined " + recruit.user.username + " from becoming a member of your alliance!")
    except AllianceRequest.DoesNotExist:
        return HttpResponse("Request not found for " + recruit.user.username)


@login_required
def get_gold(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    return HttpResponse(city.gold)


@login_required
def buy(request):
    if request.method == 'GET':
        element_type = request.GET['element_type']
    else:
        return HttpResponse("-2")

    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    cost = Cost.objects.all().get()

    if element_type == 'house':
        temp_cost = calc_house_price(cost.house_price, city.house_level)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.house_level += 1
            city.save()
            return HttpResponse(str(city.house_level) + "," + str(city.get_maximum_troops()) + "," + str(
                calc_house_price(cost.house_price, city.house_level)))
    if element_type == 'wall':
        temp_cost = calc_wall_price(cost.wall_price, city.walls_level)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.walls_level += 1
            city.save()
            return HttpResponse(str(city.walls_level) + "," + str(calc_wall_price(cost.wall_price, city.walls_level)))
    if element_type == 'lands':
        temp_cost = calc_lands_price(cost.lands_price, city.lands_owned)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.lands_owned += 1
            city.save()
            return HttpResponse(str(city.lands_owned) + "," + str(calc_lands_price(cost.lands_price, city.lands_owned)))
    if city.footmen + city.bowmen + city.knights + city.war_machines < city.get_maximum_troops():
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
    else:
        return HttpResponse("-3")
    return HttpResponse("-1")


def calc_house_price(base, level):
    return base * (level + 1)


def calc_lands_price(base, level):
    return base * (level + 1)


def calc_wall_price(base, level):
    return base * (level + 1)


@login_required
def kick_member(request, member):
    user = User.objects.get(pk=request.user.pk)
    admin = Account.objects.get(user=user)
    other_member = User.objects.get(username=member)
    poor_member = Account.objects.get(user=other_member)
    if admin.alliance_owner:
        poor_member.alliance = None
        poor_member.save()
        return HttpResponse("1")
    else:
        return HttpResponse("-1")


@login_required
def attack(request, opponent):
    enemy = User.objects.get(username=opponent)
    enemyaccount = Account.objects.get(user=enemy)
    ecity = City.objects.all().get(account=enemyaccount)
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)

    if city.footmen + (city.bowmen * 1.5) + (city.knights * 2) + (city.war_machines * 4) > (
                        ecity.footmen + (ecity.bowmen * 1.5) + (ecity.knights * 2) + (ecity.war_machines * 4)) * (
                (10 + ecity.walls_level) / 10):
        rnggold = randint(10, 15)
        tempgold = ecity.gold / rnggold
        loseArmy(city, ecity, False, True, enemy, tempgold)
        loseArmy(ecity, city, True, False, user, tempgold)
        print "victory"
        return HttpResponse("victory")
    else:
        rnggold = randint(5, 10)
        tempgold = city.gold / rnggold
        loseArmy(city, ecity, False, False, enemy, tempgold)
        loseArmy(ecity, city, True, True, user, tempgold)
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
        return HttpResponse("-1")

    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        # create alliance
        created_alliance = Alliance.objects.create(name=name, description=desc)
        created_alliance.save()
    except Alliance.IntegrityError:
        return HttpResponse("-2")
    # alliance successfully created
    acc.alliance = created_alliance
    acc.alliance_owner = True
    acc.save();
    return HttpResponse("1")


@login_required
def alliance_search(request, query):
    similar_alliances = Alliance.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context_dict = {'similar_alliances': similar_alliances, 'query': query}
    return render(request, 'game/alliance_search.html', context_dict)


@login_required
def alliance_search_empty(request):
    similar_alliances = Alliance.objects.order_by('-all_time_score')[:10]
    context_dict = {'similar_alliances': similar_alliances, 'query': ""}
    return render(request, 'game/alliance_search.html', context_dict)


def get_correct_image(house_level):
    return 1 + (int(house_level) / 10)


@login_required
def city_img(request, house_level):
    city_pic = CityGraphic.objects.get(level=get_correct_image(house_level))
    return HttpResponse(str(city_pic.picture))
