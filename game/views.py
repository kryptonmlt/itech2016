from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from game.models import Account, Alliance, AllianceRequest, City, Badge, Log, Message, Cost, CityGraphic, \
    AllianceMessage
from django.contrib.auth.models import User
from game.forms import CityForm
from django.utils import timezone
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
                create_log(acc, "Welcome to the game " + acc.user.username + " owner of " + city.name)
            else:
                err_msg = "Form was not valid!"
        if city is None:
            city_form = CityForm()
            return render(request, 'game/create_city.html', {'city_form': city_form, 'acc': acc, 'err_msg': err_msg})

    userlist = Account.objects.exclude(user=request.user)
    cost.wall_price = cost.calc_wall_price(city.walls_level)
    cost.farms_price = cost.calc_farms_price(city.farms)
    cost.stone_caves_price = cost.calc_caves_price(city.stone_caves)
    cost.gold_mines_price = cost.calc_mines_price(city.gold_mines)
    cost.lumber_mills_price = cost.calc_mills_price(city.lumber_mills)
    city_pic = CityGraphic.objects.get(level=get_correct_image(city.walls_level))
    context_dict = {'userlist': userlist, 'cost': cost, 'city': city, 'acc': acc, 'city_pic': city_pic}
    return render(request, 'game/game.html', context_dict)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


@login_required
def collect(request):
    hours = 4
    seconds = hours * 60 * 60
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    result = "DONE," + str(seconds)
    time_left = acc.received_resources_in(hours)
    if time_left > 0:
        result = "WAIT," + str(time_left)
    else:
        cost = Cost.objects.all().get()
        # account received resources now
        acc.last_received_gold = timezone.now()
        acc.save()
        # update city resources
        city = City.objects.get(account=acc)
        gold_gained = cost.calc_gold_income(city.gold_mines)
        lumber_gained = cost.calc_lumber_income(city.lumber_mills)
        stone_gained = cost.calc_stone_income(city.stone_caves)
        city.gold += gold_gained
        city.lumber += lumber_gained
        city.stones += stone_gained
        create_log(acc, "Your structures have generated " + str(gold_gained) + " gold, " + str(
            lumber_gained) + " lumber, " + str(
            stone_gained) + " stones")
        city.save()
    return HttpResponse(result)


@login_required
def last_attacked(request, enemy_acc_id):
    hours = 4
    seconds = hours * 60 * 60
    enemy = Account.objects.get(pk=enemy_acc_id)
    result = "DONE," + str(seconds)
    time_left = enemy.attacked_in_last(hours)
    if time_left > 0:
        result = "WAIT," + str(time_left)
    return HttpResponse(result)


@login_required
def get_logs(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        last_log_id = request.GET['latest_log_id']
        if last_log_id == "-1":
            logs = Log.objects.all().filter(account=acc).order_by('date_occurred')[:10]
        else:
            logs = Log.objects.all().filter(account=acc, pk__gt=last_log_id).order_by('date_occurred')
    except MultiValueDictKeyError:
        logs = Log.objects.all().filter(account=acc).order_by('date_occurred')[:10]
    return HttpResponse(logs)


@login_required
def get_messages(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        to_account_id = request.GET['to_account_id']
        last_message_id = request.GET['last_message_id']
        other_account = Account.objects.get(pk=to_account_id)
        if last_message_id == "-1":
            messages = Message.objects.all().filter(
                Q(from_account=other_account, to_account=acc) | Q(from_account=acc, to_account=other_account)).order_by(
                'date_occurred')[:10]
        else:
            messages = Message.objects.all().filter(
                Q(from_account=other_account, to_account=acc) | Q(from_account=acc, to_account=other_account),
                pk__gt=last_message_id).order_by('date_occurred')
    except MultiValueDictKeyError:
        try:
            to_account_id = request.GET['to_account_id']
            other_account = Account.objects.get(pk=to_account_id)
            messages = Message.objects.all().filter(
                Q(from_account=other_account, to_account=acc) | Q(from_account=acc, to_account=other_account)).order_by(
                'date_occurred')[:10]
        except MultiValueDictKeyError:
            return HttpResponse("-1")
    return HttpResponse(messages)


@login_required
def add_message(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        message = request.GET['message']
        to_account_id = request.GET['to_account_id']
        other_account = Account.objects.get(pk=to_account_id)
        m = Message.objects.create(from_account=acc, to_account=other_account, text=message)
        m.save()
    except MultiValueDictKeyError:
        return HttpResponse("-1")
    return HttpResponse("1")


@login_required
def add_alliance_message(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        message = request.GET['message']
        to_alliance_id = request.GET['to_alliance_id']
        other_alliance = Alliance.objects.get(pk=to_alliance_id)
        am = AllianceMessage.objects.create(from_account=acc, to_alliance=other_alliance, text=message)
        am.save()
    except MultiValueDictKeyError:
        return HttpResponse("-1")
    return HttpResponse("1")


@login_required
def get_alliance_messages(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    try:
        last_message_id = request.GET['last_message_id']
        if last_message_id == "-1":
            messages = AllianceMessage.objects.all().filter(Q(to_alliance=acc.alliance) | Q(from_account=acc)).order_by(
                'date_occurred')[
                       :10]
        else:
            messages = AllianceMessage.objects.all().filter(Q(to_alliance=acc.alliance) | Q(from_account=acc),
                                                            pk__gt=last_message_id).order_by('date_occurred')
    except MultiValueDictKeyError:
        messages = AllianceMessage.objects.all().filter(Q(to_alliance=acc.alliance) | Q(from_account=acc)).order_by(
            'date_occurred')[:10]
    return HttpResponse(messages)


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
        extra_info = ""
        if acc.alliance_owner:
            next_in_line = \
                Account.objects.all().filter(alliance=acc.alliance).exclude(user=request.user).order_by('-wins')
            if next_in_line.count() > 0:  # appoint next in line as leader
                next_leader = next_in_line[0]
                next_leader.alliance_owner = True
                next_leader.save()
                extra_info = ", " + next_leader.user.username + " is your successor"
                create_log(next_leader,
                           "You became the new leader of the alliance " + next_leader.alliance.name + ", after" + acc.user.username + " left.")
                reply = "Next in line (" + next_leader.user.username + ") now leader of alliance, "
            else:  # delete alliance since no one left to take it
                extra_info = ", alliance was disbanded due to no successors"
                acc.alliance.delete()
                reply = "No one next in line, alliance collapsed, "
        create_log(acc,
                   "You left the alliance " + acc.alliance.name + extra_info)
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
@login_required
def get_resources(request):
    user = User.objects.get(pk=request.user.pk)
    acc = Account.objects.get(user=user)
    city = City.objects.all().get(account=acc)
    return HttpResponse(str(city.gold) + "," + str(city.lumber) + "," + str(city.stones))


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

    if element_type == 'wall':
        temp_cost = cost.calc_wall_price(city.walls_level).split(',')
        if city.gold >= int(temp_cost[0]):
            if city.lumber >= int(temp_cost[1]):
                if city.stones >= int(temp_cost[2]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.stones -= int(temp_cost[2])
                    city.walls_level += 1
                    city.save()
                    return HttpResponse(str(city.walls_level) + "," + cost.calc_wall_price(city.walls_level))
                else:
                    return HttpResponse("-3")
            else:
                return HttpResponse("-2")
        else:
            return HttpResponse("-1")

    if element_type == 'farms':
        temp_cost = cost.calc_farms_price(city.farms).split(',')
        if city.gold >= int(temp_cost[0]):
            if city.lumber >= int(temp_cost[1]):
                if city.stones >= int(temp_cost[2]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.stones -= int(temp_cost[2])
                    city.farms += 1
                    city.save()
                    return HttpResponse(
                        str(city.farms) + "," + str(city.get_maximum_troops()) + "," + cost.calc_farms_price(
                            city.farms))
                else:
                    return HttpResponse("-3")
            else:
                return HttpResponse("-2")
        else:
            return HttpResponse("-1")
    if element_type == 'gold_mines':
        temp_cost = cost.calc_mines_price(city.gold_mines).split(',')
        if city.gold >= int(temp_cost[0]):
            if city.lumber >= int(temp_cost[1]):
                if city.stones >= int(temp_cost[2]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.stones -= int(temp_cost[2])
                    city.gold_mines += 1
                    city.save()
                    return HttpResponse(str(city.gold_mines) + "," + str(cost.calc_mines_price(city.gold_mines)))
                else:
                    return HttpResponse("-3")
            else:
                return HttpResponse("-2")
        else:
            return HttpResponse("-1")
    if element_type == 'stone_caves':
        temp_cost = cost.calc_caves_price(city.stone_caves).split(',')
        if city.gold >= int(temp_cost[0]):
            if city.lumber >= int(temp_cost[1]):
                if city.stones >= int(temp_cost[2]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.stones -= int(temp_cost[2])
                    city.stone_caves += 1
                    city.save()
                    return HttpResponse(str(city.stone_caves) + "," + cost.calc_caves_price(city.stone_caves))
                else:
                    return HttpResponse("-3")
            else:
                return HttpResponse("-2")
        else:
            return HttpResponse("-1")
    if element_type == 'lumber_mills':
        temp_cost = cost.calc_mills_price(city.lumber_mills).split(',')
        if city.gold >= int(temp_cost[0]):
            if city.lumber >= int(temp_cost[1]):
                if city.stones >= int(temp_cost[2]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.stones -= int(temp_cost[2])
                    city.lumber_mills += 1
                    city.save()
                    return HttpResponse(str(city.lumber_mills) + "," + cost.calc_mills_price(city.lumber_mills))
                else:
                    return HttpResponse("-3")
            else:
                return HttpResponse("-2")
        else:
            return HttpResponse("-1")

    if city.footmen + city.bowmen + city.knights + city.war_machines < city.get_maximum_troops():
        if element_type == 'footmen':
            if city.gold >= cost.footmen_price:
                city.gold -= cost.footmen_price
                city.footmen += 1
                city.save()
                return HttpResponse(city.footmen)
            else:
                return HttpResponse("-1")
        if element_type == 'bowmen':
            if city.gold >= cost.bowmen_price:
                city.gold -= cost.bowmen_price
                city.bowmen += 1
                city.save()
                return HttpResponse(city.bowmen)
            else:
                return HttpResponse("-1")
        if element_type == 'knights':
            if city.gold >= cost.knights_price:
                city.gold -= cost.knights_price
                city.knights += 1
                city.save()
                return HttpResponse(city.knights)
            else:
                return HttpResponse("-1")
        if element_type == 'war_machines':
            temp_cost = cost.calc_war_machines_price().split(',')
            if city.gold >= int(temp_cost[0]):
                if city.lumber >= int(temp_cost[1]):
                    city.gold -= int(temp_cost[0])
                    city.lumber -= int(temp_cost[1])
                    city.war_machines += 1
                    city.save()
                    return HttpResponse(city.war_machines)
                else:
                    return HttpResponse("-2")
            else:
                return HttpResponse("-1")
    else:
        return HttpResponse("-4")


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

    enemyaccount.last_attacked = timezone.now()
    if city.footmen + (city.bowmen * 1.5) + (city.knights * 2) + (city.war_machines * 4) > (
                        ecity.footmen + (ecity.bowmen * 1.5) + (ecity.knights * 2) + (ecity.war_machines * 4)) * (
                (10 + ecity.walls_level) / 10):
        rnggold = randint(10, 15)
        tempgold = ecity.gold / rnggold
        result = lose_army(city, ecity, False, True, tempgold)
        lose_army(ecity, city, True, False, tempgold)
        acc.wins += 1
        enemyaccount.defeats += 1
    else:
        rnggold = randint(5, 10)
        tempgold = city.gold / rnggold
        result = lose_army(city, ecity, False, False, tempgold)
        lose_army(ecity, city, True, True, tempgold)
        acc.defeats += 1
        enemyaccount.wins += 1
    enemyaccount.save()
    acc.save()
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

    footmenlost = city.footmen * rng / 100
    city.footmen -= footmenlost
    bowmenlost = city.footmen * rng / 100
    city.bowmen -= bowmenlost
    knightslost = city.knights * rng / 100
    city.knights -= knightslost
    war_machineslost = city.war_machines * rng / 100
    city.war_machines -= war_machineslost

    ecity.save()
    city.save()

    if winner:
        result = "You defeated " + ecity.account.user.username + " gaining " + str(
            tempgold) + " gold coins from your enemy and losing:\n"
    else:
        result = "You suffered a defeat from " + ecity.account.user.username + " losing " + str(
            tempgold) + " gold coins along with:\n"
    return result + str(footmenlost) + " Footmen \n" + str(bowmenlost) + " Bowmen \n" + str(
        knightslost) + " Knights \n" + str(war_machineslost) + " War Machines\n"


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
    acc.save()
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


def get_correct_image(walls_level):
    return 1 + (int(walls_level) / 10)


@login_required
def city_img(request, walls_level):
    city_pic = CityGraphic.objects.get(level=get_correct_image(walls_level))
    return HttpResponse(str(city_pic.picture))


def create_log(account, text):
    log = Log.objects.create(account=account, text=text)
    log.save()


@login_required
def get_map(request):
    max_x = City.objects.all().order_by("-x")[0].x
    max_y = City.objects.all().order_by("-y")[0].y
    map_size_interval = 100
    map_proportion_x = (max_x / map_size_interval) + map_size_interval
    map_proportion_y = (max_y / map_size_interval) + map_size_interval

    matrix = [[0 for x in range(map_proportion_x)] for y in range(map_proportion_y)]

    cities = City.objects.all()
    for city in cities:
        print city
        matrix[city.x][city.y] = city.account.user.username

    tile_map = ""
    for y in range(map_proportion_y):
        for x in range(map_proportion_x):
            tile_map += str(matrix[x][y]);
        tile_map += ";";
    return HttpResponse(tile_map)
