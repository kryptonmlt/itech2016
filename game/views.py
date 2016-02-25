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
    cost.houses_price = calc_houses_price(cost.houses_price, city.houses_level)
    cost.farms_price = calc_farms_price(cost.farms_price, city.farms)
    cost.stone_caves_price = calc_caves_price(cost.stone_caves_price, city.stone_caves)
    cost.gold_mines_price = calc_mines_price(cost.gold_mines_price, city.gold_mines)
    cost.lumber_mills_price = calc_mills_price(cost.lumber_mills_price, city.lumber_mills)
    city_pic = CityGraphic.objects.get(level=get_correct_image(city.houses_level))
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
    try:
        last_log_id = request.GET['latest_log_id']
        if last_log_id == -1:
            logs = Log.objects.all().filter(account=acc).order_by('date_occurred')[:10]
        else:
            logs = Log.objects.all().filter(account=acc, pk__gt=last_log_id).order_by('date_occurred')
    except MultiValueDictKeyError:
        logs = Log.objects.all().filter(account=acc).order_by('date_occurred')[:10]
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
def change_orders(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    if acc.alliance_owner:
        if request.method == 'GET':
            orders = request.GET['orders']
            acc.alliance.orders = orders
            acc.alliance.save()
            members = Account.objects.all().filter(alliance=acc.alliance)
            for member in members:
                create_log(member, "Leader " + acc.user.username + " gave out new orders!")

            return HttpResponse("1")
    return HttpResponse("-1")


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
        all_req = AllianceRequest.objects.create(from_account=acc, alliance=alli, text=msg)
        all_req.save()
        create_log(acc, "You sent a request to join alliance " + alli.name)
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
                create_log(acc,
                           "You left the alliance " + acc.alliance.name + ", " + next_leader.user.username + " is your successor")
                create_log(next_leader, "You approved " + acc.user.username + " to becoming a member of your alliance!")
                reply = "Next in line (" + next_leader.user.username + ") now leader of alliance, "
            else:  # delete alliance since no one left to take it
                create_log(acc,
                           "You left the alliance " + acc.alliance.name + ", alliance was disbanded due to no successors")
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
            create_log(recruit,
                       "You are now a member of " + req.alliance.name + ", request was accepted by alliance leader " + leader.user.username)
            create_log(leader, "You approved " + recruit.user.username + " to becoming a member of your alliance!")
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
        create_log(recruit,
                   "Your request to join " + req.alliance.name + " was declined by alliance leader " + leader.user.username)
        create_log(leader, "You declined " + recruit.user.username + " from becoming a member of your alliance!")
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
def get_lumber(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    return HttpResponse(city.lumber)

@login_required
def get_stones(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    return HttpResponse(city.stones)

@login_required
def get_food(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    return HttpResponse(city.food)


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

    if element_type == 'houses':
        temp_cost = calc_houses_price(cost.houses_price, city.houses_level)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.houses_level += 1
            city.save()
            return HttpResponse(str(city.houses_level) + "," + str(city.get_maximum_troops()) + "," + str(
                calc_houses_price(cost.houses_price, city.houses_level)))
    if element_type == 'wall':
        temp_cost = calc_wall_price(cost.wall_price, city.walls_level)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.walls_level += 1
            city.save()
            return HttpResponse(str(city.walls_level) + "," + str(calc_wall_price(cost.wall_price, city.walls_level)))
    if element_type == 'farms':
        temp_cost = calc_farms_price(cost.farms_price, city.farms)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.farms += 1
            city.save()
            return HttpResponse(str(city.farms_owned) + "," + str(calc_farms_price(cost.farms_price, city.farms)))
    if element_type == 'gold_mines':
        temp_cost = calc_mines_price(cost.gold_mines_price, city.gold_mines)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.gold_mines += 1
            city.save()
            return HttpResponse(str(city.gold_mines) + "," + str(calc_mines_price(cost.gold_mines_price, city.gold_mines)))
    if element_type == 'stone_caves':
        temp_cost = calc_caves_price(cost.stone_caves_price, city.stone_caves)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.stone_caves += 1
            city.save()
            return HttpResponse(str(city.stone_caves) + "," + str(calc_caves_price(cost.stone_caves_price, city.stone_caves)))
    if element_type == 'lumber_mills':
        temp_cost = calc_mills_price(cost.lumber_mills_price, city.lumber_mills)
        if city.gold >= temp_cost:
            city.gold -= temp_cost
            city.lumber_mills += 1
            city.save()
            return HttpResponse(str(city.lumber_mills) + "," + str(calc_mills_price(cost.lumber_mills_price, city.lumber_mills)))
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


def calc_houses_price(base, level):
    return base * (level + 1)

def calc_farms_price(base, level):
    return base * (level + 1)

def calc_wall_price(base, level):
    return base * (level + 1)

def calc_mills_price(base, level):
    return base * (level + 1)

def calc_caves_price(base, level):
    return base * (level + 1)

def calc_mines_price(base, level):
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
        create_log(admin, "you kicked " + poor_member.user.username + " from the alliance")
        create_log(poor_member, "you were kicked from the alliance under the rule of Leader " + admin.user.username)
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
        result = lose_army(city, ecity, False, True, tempgold)
        lose_army(ecity, city, True, False, tempgold)
        return HttpResponse(result)
    else:
        rnggold = randint(5, 10)
        tempgold = city.gold / rnggold
        result = lose_army(city, ecity, False, False, tempgold)
        lose_army(ecity, city, True, True, tempgold)
        return HttpResponse(result)


def lose_army(city, ecity, defender, winner, tempgold):
    if defender:
        if winner:
            rng = randint(5, 15)
            city.gold += tempgold
            ecity.gold -= tempgold
            create_win_log(city.account, ecity.account, rng, defender, tempgold)
        else:
            rng = randint(15, 30)
            create_defeat_log(city.account, ecity.account, rng, defender, tempgold)
            city.gold -= tempgold
            ecity.gold += tempgold
    else:
        if winner:
            rng = randint(15, 30)
            create_win_log(city.account, ecity.account, rng, defender, tempgold)
            city.gold += tempgold
            ecity.gold -= tempgold
        else:
            rng = randint(30, 50)
            create_defeat_log(city.account, ecity.account, rng, defender, tempgold)
            city.gold -= tempgold
            ecity.gold += tempgold

    footmenlost=city.footmen * rng / 100
    city.footmen -= footmenlost
    bowmenlost=city.footmen * rng / 100
    city.bowmen -= bowmenlost
    knightslost=city.knights * rng / 100
    city.knights -= knightslost
    war_machineslost=city.war_machines * rng / 100
    city.war_machines -= war_machineslost

    ecity.save()
    city.save()

    if winner:
        result= "You defeated " + ecity.account.user.username+ " gaining " + str(tempgold) + " gold coins from your enemy and losing:\n"
    else:
        result="You suffered a defeat from " + ecity.account.user.username + " losing "+ str(tempgold) + " gold coins along with:\n"
    return result+str(footmenlost)+" Footmen \n"+str(bowmenlost)+" Bowmen \n"+str(knightslost)+" Knights \n"+str(war_machineslost)+" War Machines"


def create_win_log(account, enemy_account, casualties, defender, tempgold):
    if defender:
        log = Log.objects.create(account=account,
                                 text="Your troops managed to defend the city successfully from " + enemy_account.user.username + ", but lost " + str(
                                     casualties) + " % of your troops and gained " + str(
                                     tempgold) + " gold coins from your enemy")
    else:
        log = Log.objects.create(account=account, text="You defeated " + enemy_account.user.username + " losing " + str(
            casualties) + " % of your troops and gaining " + str(tempgold) + " gold coins from your enemy")
    log.save()


def create_defeat_log(account, enemy_account, casualties, defender, tempgold):
    if defender:
        log = Log.objects.create(account=account,
                                 text="You failed to defend your city from " + enemy_account.user.username + " losing " + str(
                                     casualties) + " % of your troops along with " + str(tempgold) + " gold coins")
    else:
        log = Log.objects.create(account=account,
                                 text="You suffered a defeat from " + enemy_account.user.username + " losing " + str(
                                     casualties) + " % of your troops along with " + str(tempgold) + " gold coins")
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
    # create alliance
    created_alliance = Alliance.objects.create(name=name, description=desc)
    created_alliance.save()
    # alliance successfully created
    acc.alliance = created_alliance
    acc.alliance_owner = True
    acc.save();
    create_log(acc, "Let it be known, " + acc.user.username + " just founded the alliance " + acc.alliance.name)
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


def create_log(account, text):
    log = Log.objects.create(account=account, text=text)
    log.save()
