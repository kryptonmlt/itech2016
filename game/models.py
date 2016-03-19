import datetime

from django.db import models
from django.utils import timezone
from django.utils import formats
from django.contrib.auth.models import User
from random import randint
from django.template.defaultfilters import slugify


class Alliance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    all_time_score = models.IntegerField(default=0)
    orders = models.CharField(max_length=300)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Alliance, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, default=None)
    picture = models.ImageField(upload_to='portraits', blank=True)
    last_attacked = models.DateTimeField('date attacked', default=None, null=True, blank=True)
    last_received_gold = models.DateTimeField('date received gold', default=timezone.now)
    wins = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)
    alliance_owner = models.BooleanField(default=False)
    alliance = models.ForeignKey(Alliance, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def attacked_in_last(self, hours):
        now = timezone.now()
        delta = now - self.last_attacked
        hours_passed = delta.total_seconds() // 3600
        if hours_passed >= hours:
            return 0
        else:
            time_remaining = datetime.timedelta(hours=hours) - delta
            return time_remaining.total_seconds()

    def received_resources_in(self, hours):
        now = timezone.now()
        delta = now - self.last_received_gold
        hours_passed = delta.total_seconds() // 3600
        if hours_passed >= hours:
            return 0
        else:
            time_remaining = datetime.timedelta(hours=hours) - delta
            return time_remaining.total_seconds()

    def get_win_percentage(self):
        if self.defeats == 0 and self.wins == 0:
            return 0
        else:
            return int((self.wins / float((self.defeats + self.wins))) * 100)


class City(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    gold = models.IntegerField(default=1000)
    lumber = models.IntegerField(default=100)
    stones = models.IntegerField(default=100)
    farms = models.IntegerField(default=1)
    walls_level = models.IntegerField(default=0)
    lumber_mills = models.IntegerField(default=1)
    stone_caves = models.IntegerField(default=1)
    gold_mines = models.IntegerField(default=1)
    footmen = models.IntegerField(default=0)
    bowmen = models.IntegerField(default=0)
    knights = models.IntegerField(default=0)
    war_machines = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        # place city somewhere on map
        if self.id is None:

            map_size_interval = 100
            minimum_distance_x = 4
            minimum_distance_y = 0
            maximum_distance_x = 6
            maximum_distance_y = 2
            row_separator = 6

            # first city check
            try:
                max_x = City.objects.all().order_by("-x")[0].x
            except IndexError:
                max_x = 0

            dist_x = randint(minimum_distance_x, maximum_distance_x)
            dist_y = randint(minimum_distance_y, maximum_distance_y) - 2

            map_proportion = (max_x / map_size_interval) + 1

            map_info = MapInfo.objects.get(pk=1)

            if (map_info.current_x_in_row + dist_x + 2) < (map_proportion * map_size_interval):
                # less than max width
                chosen_x = map_info.current_x_in_row + dist_x
                chosen_y = map_info.current_y_row + dist_y

                map_info.current_x_in_row += dist_x
            else:
                # greater than max width
                if (map_info.current_y_row + row_separator) < (map_proportion * map_size_interval):
                    # new row
                    chosen_x = dist_x
                    chosen_y = map_info.current_y_row + row_separator + dist_y

                    map_info.current_x_in_row = dist_x
                    map_info.current_y_row += row_separator
                else:
                    # increase map width size
                    chosen_x = map_info.current_x_in_row + dist_x
                    chosen_y = row_separator + dist_y

                    map_info.current_x_in_row += dist_x
                    map_info.current_y_row = row_separator

            map_info.save()
            self.x = chosen_x
            self.y = chosen_y
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + "(" + str(self.x) + "," + str(self.y) + ")"

    def get_maximum_troops(self):
        return 50 * self.farms

    def get_total_troops(self):
        return self.footmen + self.knights + self.bowmen + self.war_machines

    def army_total(self):
        return self.footmen + self.bowmen + self.knights + self.war_machines


class MapInfo(models.Model):
    current_x_in_row = models.IntegerField(default=0)
    current_y_row = models.IntegerField(default=5)

    def __str__(self):
        return "(" + str(self.current_x_in_row) + "," + str(self.current_y_row) + ")"


class AllianceRequest(models.Model):
    from_account = models.ForeignKey(Account, related_name="from_account_alliance_request")
    alliance = models.ForeignKey(Alliance, related_name="alliance_owner_request", default=None, null=True, blank=True)
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred', default=timezone.now)

    def __str__(self):
        return self.from_account.user.username + " asking " + self.alliance.name


class Message(models.Model):
    from_account = models.ForeignKey(Account, related_name="from_account_messages")
    to_account = models.ForeignKey(Account, related_name="to_account_messages")
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred', default=timezone.now)

    def __str__(self):
        return str(self.pk) + "||" + self.from_account.user.username + "||" + self.text + "$$"


class AllianceMessage(models.Model):
    from_account = models.ForeignKey(Account, related_name="from_account_alliance_messages")
    to_alliance = models.ForeignKey(Alliance, related_name="to_alliance_messages")
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred', default=timezone.now)

    def __str__(self):
        return str(self.pk) + "||" + self.from_account.user.username + "||" + self.text + "$$"


class Badge(models.Model):
    account = models.ForeignKey(Account, related_name="account_badges")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.account.user.username + " " + self.name


class Log(models.Model):
    account = models.ForeignKey(Account, related_name="account_logs", default=None, null=True, blank=True)
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred', default=timezone.now)

    def __str__(self):
        dif = timezone.now() - self.date_occurred
        if dif.days > 0:
            dif = '{0} d'.format(dif.days)
        else:
            seconds = dif.total_seconds()
            if seconds // 3600 > 0:
                dif = '{:.0f} h'.format(seconds // 3600)
            elif (seconds % 3600) // 60 > 0:
                dif = '{:.0f} m'.format((seconds % 3600) // 60)
            elif seconds % 60 > 1:
                dif = '{:.0f} s'.format(seconds % 60)
            else:
                dif = 'now'
                
        return str(self.pk) + "||" + str(dif) + "||" + self.text + "$$"


class Cost(models.Model):
    footmen_price = models.IntegerField(default=10)
    bowmen_price = models.IntegerField(default=15)
    knights_price = models.IntegerField(default=25)
    war_machines_price = models.CharField(max_length=100, default="40,10")
    wall_price = models.CharField(max_length=100, default="1000,100,200")
    farms_price = models.CharField(max_length=100, default="200,100,100")
    lumber_mills_price = models.CharField(max_length=100, default="200,200,100")
    stone_caves_price = models.CharField(max_length=100, default="200,150,150")
    gold_mines_price = models.CharField(max_length=100, default="300,150,150")
    gold_income = models.IntegerField(default=100)
    lumber_income = models.IntegerField(default=25)
    stone_income = models.IntegerField(default=25)

    def __str__(self):
        return "Cost stats"

    def calc_farms_price(self, level):
        prices = self.farms_price.split(',')
        return str(int(prices[0]) * (level + 1)) + "," + str(int(prices[1]) * (level + 1)) + "," + str(
            int(prices[2]) * (level + 1))

    def calc_wall_price(self, level):
        prices = self.wall_price.split(',')
        return str(int(prices[0]) * (level + 1)) + "," + str(int(prices[1]) * (level + 1)) + "," + str(
            int(prices[2]) * (level + 1))

    def calc_mills_price(self, level):
        prices = self.lumber_mills_price.split(',')
        return str(int(prices[0]) * (level + 1)) + "," + str(int(prices[1]) * (level + 1)) + "," + str(
            int(prices[2]) * (level + 1))

    def calc_caves_price(self, level):
        prices = self.stone_caves_price.split(',')
        return str(int(prices[0]) * (level + 1)) + "," + str(int(prices[1]) * (level + 1)) + "," + str(
            int(prices[2]) * (level + 1))

    def calc_mines_price(self, level):
        prices = self.gold_mines_price.split(',')
        return str(int(prices[0]) * (level + 1)) + "," + str(int(prices[1]) * (level + 1)) + "," + str(
            int(prices[2]) * (level + 1))

    def calc_war_machines_price(self):
        prices = self.war_machines_price.split(',')
        return str(int(prices[0])) + "," + str(int(prices[1]))

    def calc_gold_income(self, level):
        return self.gold_income * level

    def calc_stone_income(self, level):
        return self.stone_income * level

    def calc_lumber_income(self, level):
        return self.lumber_income * level
