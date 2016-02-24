import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech2016.settings')

import django

django.setup()

from django.contrib.auth.models import User
from datetime import datetime

from game.models import Alliance, Account, City, AllianceRequest, Message, Badge, Log, Cost, CityGraphic


def populate():
    u1 = add_user('Ruben', 'Ruben@gmail.com', '1234')
    u2 = add_user('Florian', 'Florian@gmail.com', '1234')
    u3 = add_user('Kurt', 'Kurt@gmail.com', '1234')
    u4 = add_user('Pedro', 'Pedro@gmail.com', '1234')

    al1 = add_alliance('Rubens_alliance', 'this is rubens alliance', 100)
    al2 = add_alliance('Kurtman_rules', 'this is kurts alliance', 300)

    a1 = add_account(u1, 7, 15, True, al1, 'Ruben')
    a2 = add_account(u2, 40, 10, False, al1, 'Florian')
    a3 = add_account(u3, 20, 1, True, al2, 'Kurt')
    a4 = add_account(u4, 10, 10, False, al1, 'Pedro')

    c1 = add_city(a1, 'Rubens Kindom', 40, 5, 2, 7, 10, 10, 10, 10)
    c2 = add_city(a2, 'Florians Kindom', 1000, 10, 0, 2, 20, 40, 10, 10)
    c3 = add_city(a3, 'Kurtmans Kindom', 9993923, 5, 3, 2, 10, 20, 0, 10)
    c4 = add_city(a4, 'Pedros Kindom', 1234, 100, 2, 0, 2, 10, 10, 50)

    add_log(c1, 'you got attacked by kurtman')
    add_log(c1, 'kurtman won!')
    add_log(c1, 'you lost 100 gold')

    add_log(c3, 'you attacked ruben')
    add_log(c3, 'you won!')
    add_log(c3, 'you won 100 gold')

    add_log(c2, 'welcome to the game')
    add_log(c4, 'welcome to the game')

    add_badge(a1, 'Lost 10 games in a row!')
    add_badge(a1, 'Won 5 games in a row!')

    add_badge(a2, 'Played 10 days in a row')

    add_badge(a3, 'Won 10 games in a row!')

    add_badge(a4, 'Lost all of his army in battle')

    add_message(a1, a3, 'good game')
    add_message(a3, a2, 'what was that')
    add_message(a1, a4, 'you are good')

    for x in range(0, 50):
        add_city_graphic(x, 'media/city/' + str(x) + '.png')

    add_costs()


def add_user(name, email, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.email = email
    u.save()
    return u


def add_account(user, wins, defeats, alliance_owner, alliance, picture):
    a = Account.objects.get_or_create(user=user)[0]
    a.last_attacked = datetime.now()
    a.last_received_gold = datetime.now()
    a.wins = wins
    a.defeats = defeats
    a.alliance_owner = alliance_owner
    a.alliance = alliance
    a.picture = 'media/' + picture
    a.save()
    return a


def add_city_graphic(level, picture):
    cg = CityGraphic.objects.create(level=level, picture=picture)
    cg.save()


def add_alliance(name, description, all_time_score):
    a = Alliance.objects.get_or_create(name=name)[0]
    a.description = description
    a.all_time_score = all_time_score
    a.save()
    return a


def add_city(account, name, gold, house_level, lands_owned, walls_level, footmen, bowmen, knights, war_machines):
    c = City.objects.get_or_create(account=account)[0]
    c.name = name
    c.gold = gold
    c.house_level = house_level
    c.lands_owned = lands_owned
    c.walls_level = walls_level
    c.footmen = footmen
    c.bowmen = bowmen
    c.knights = knights
    c.war_machines = war_machines
    c.save()
    return c


def add_log(city, text):
    l = Log.objects.get_or_create(city=city, date_occurred=datetime.now())[0]
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


# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()
