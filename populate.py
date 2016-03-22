import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech2016.settings')

import django

django.setup()

from django.contrib.auth.models import User
from datetime import datetime, timedelta

from game.models import Alliance, Account, City, AllianceRequest, Message, Badge, Log, Cost, MapInfo


def populate():
    add_map_info()

    devs = add_alliance('the devs', 'developers', 100)
    kurt = add_user_account_city_log_badge('Kurt', 'kurtporteli@gmail.com', '1234', devs, True)
    ruben = add_user_account_city_log_badge('Ruben', 'ruben.giaquinta@gmail.com', '1234', devs, False)
    florian = add_user_account_city_log_badge('Florian', 'florian.deuerlein@gmail.com', '1234', devs, False)
    pedro = add_user_account_city_log_badge('Pedro', 'phoquintas@gmail.com', '1234', devs, False)

    lecs = add_alliance('itech2016', 'lecturers and tutors', 0)
    leifos = add_user_account_city_log_badge('leifos', 'Leif.Azzopardi@glasgow.ac.uk', 'leifos', lecs, True)
    laura = add_user_account_city_log_badge('laura', 'laura@gmail.com', 'laura', lecs, False)
    david = add_user_account_city_log_badge('david', 'david@gmail.com', 'david', lecs, False)

    f = open('usernames', 'r')
    current_alliance_count = 0
    for username in f:
        username = username.strip()
        if current_alliance_count == 0:
            alls = add_alliance(username + '_alliance', 'another awesome alliance', 0)
            add_user_account_city_log_badge(username, username + '@gmail.com', '1234', alls, True)
            current_alliance_count += 1
        else:
            add_user_account_city_log_badge(username, username + '@gmail.com', '1234', alls, False)
            current_alliance_count += 1
            if current_alliance_count == 30:
                current_alliance_count = 0

    add_message(leifos, laura, 'good game')
    add_message(laura, leifos, 'what was that')
    add_message(david, leifos, 'you are good')
    add_message(leifos, david, 'yeah!')
    add_message(kurt, ruben, 'close fight')
    add_message(florian, kurt, 'damn')
    add_message(ruben, florian, 'amazing')
    add_message(florian, ruben, 'lets fight!')
    add_message(pedro, ruben, 'lets fight!')
    add_message(ruben, pedro, 'Yes!')

    add_costs()


def add_user_account_city_log_badge(username, email, password, alliance, alliance_owner):
    u = add_user(username, email, password)
    a = add_account(u, 10, 10, alliance_owner, alliance)
    add_city(a, username + ' Kingdom', 10000, 1, random.randrange(1,5,1), random.randrange(1,5,1), random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1))
    add_log(a, 'Welcome to the game !')
    add_log(a, 'Your citizens awarded you with 10,000 gold to start building the city!')
    add_log(a, 'The rest is up to you .. upgrade city structures, recruit troops, make alliances, invade ..')
    add_badge(a, 'Joined the game !')
    return a


def add_user(name, email, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.email = email
    u.save()
    return u


def add_account(user, wins, defeats, alliance_owner, alliance, picture=None):
    a = Account.objects.get_or_create(user=user)[0]
    a.last_attacked = datetime.now()  - timedelta(days=1)
    a.last_received_gold = datetime.now()
    a.wins = wins
    a.defeats = defeats
    a.alliance_owner = alliance_owner
    a.alliance = alliance
    if picture is None:
        #pick random default picture
        pic_id = random.randrange(1,5,1)
        a.picture = 'media/portraits/' + str(pic_id) + '.png'
    else:
        a.picture = picture
    a.save()
    return a


def add_alliance(name, description, all_time_score):
    a = Alliance.objects.get_or_create(name=name)[0]
    a.description = description
    a.all_time_score = all_time_score
    a.save()
    return a


def add_city(account, name, gold, farms, walls_level, stone_caves, footmen, bowmen, knights, war_machines):
    c = City.objects.get_or_create(account=account)[0]
    c.name = name
    c.gold = gold
    c.farms = farms
    c.stone_caves = stone_caves
    c.walls_level = walls_level
    c.footmen = footmen
    c.bowmen = bowmen
    c.knights = knights
    c.war_machines = war_machines
    c.save()
    return c


def add_log(account, text):
    l = Log.objects.get_or_create(account=account, date_occurred=datetime.now())[0]
    l.text = text
    l.date_occurred = datetime.now()
    l.save()
    return l


def add_badge(account, name):
    b = Badge.objects.get_or_create(account=account)[0]
    b.name = name
    b.save()
    return b


def add_message(from_account, to_account, text):
    m = Message.objects.get_or_create(from_account=from_account, to_account=to_account, date_occurred=datetime.now())[0]
    m.text = text
    m.date_occurred = datetime.now()
    m.save()
    return m


def add_costs():
    c = Cost.objects.get_or_create()[0]
    return c


def add_map_info():
    m = MapInfo.objects.get_or_create()[0]
    return m


# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()
