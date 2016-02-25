import datetime

from django.db import models
from django.utils import timezone
from django.utils import formats
from django.contrib.auth.models import User


class Alliance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    all_time_score = models.IntegerField(default=0)
    orders = models.CharField(max_length=300)

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

    def was_attacked_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=12) <= now - self.last_attacked

    def get_win_percentage(self):
        if self.defeats == 0 & self.wins == 0:
            return 0
        else:
            return int((self.wins / float((self.defeats + self.wins))) * 100)

    was_attacked_recently.admin_order_field = 'last_attacked'
    was_attacked_recently.boolean = True
    was_attacked_recently.short_description = 'Attacked recently?'


class City(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    gold = models.IntegerField(default=1000)
    lumber = models.IntegerField(default=100)
    stones = models.IntegerField(default=100)
    food = models.IntegerField(default=100)
    houses_level = models.IntegerField(default=1)
    farms = models.IntegerField(default=0)
    walls_level = models.IntegerField(default=0)
    lumber_mills = models.IntegerField(default=0)
    stone_caves = models.IntegerField(default=0)
    gold_mines = models.IntegerField(default=0)
    footmen = models.IntegerField(default=0)
    bowmen = models.IntegerField(default=0)
    knights = models.IntegerField(default=0)
    war_machines = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_maximum_troops(self):
        return 50 * self.houses_level

    def army_total(self):
        return self.footmen + self.bowmen + self.knights + self.war_machines


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
        return str(
            self.date_occurred) + ": " + self.text + ", from " + self.from_account.user.username + " to " + self.to_account.user.username


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
        return str(self.pk) + "||" + formats.date_format(self.date_occurred,
                                                    "SHORT_DATETIME_FORMAT") + "||" + self.text + "$$"


class Cost(models.Model):
    footmen_price = models.IntegerField(default=10)
    bowmen_price = models.IntegerField(default=15)
    knights_price = models.IntegerField(default=25)
    war_machines_price = models.IntegerField(default=50)
    houses_price = models.IntegerField(default=100)
    wall_price = models.IntegerField(default=1000)
    farms_price = models.IntegerField(default=500)
    lumber_mills_price = models.IntegerField(default=500)
    stone_caves_price = models.IntegerField(default=500)
    gold_mines_price = models.IntegerField(default=500)
    login_gold = models.IntegerField(default=100)

    def __str__(self):
        return "Cost stats"


class CityGraphic(models.Model):
    level = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='city', blank=True)

    def __str__(self):
        return "City Lvl " + str(self.level)
