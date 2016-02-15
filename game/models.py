import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Alliance(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    all_time_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, default=None)
    picture = models.ImageField(upload_to="pic_folder/", default="pic_folder/None/no-img.jpg")
    last_login_date = models.DateTimeField('date login')
    last_attacked = models.DateTimeField('date attacked')
    last_received_gold = models.DateTimeField('date received gold')
    wins = models.IntegerField(default=0)
    defeats = models.IntegerField(default=0)
    alliance_owner = models.BooleanField(default=False)
    alliance = models.ForeignKey(Alliance)

    def __str__(self):
        return self.email

    def was_attacked_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=12) <= now - self.last_attacked

    was_attacked_recently.admin_order_field = 'last_attacked'
    was_attacked_recently.boolean = True
    was_attacked_recently.short_description = 'Attacked recently?'


class City(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100)
    gold = models.IntegerField(default=100)
    supply = models.IntegerField(default=0)
    walls_level = models.IntegerField(default=0)
    footmen = models.IntegerField(default=0)
    bowmen = models.IntegerField(default=0)
    knights = models.IntegerField(default=0)
    war_machines = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AllianceRequest(models.Model):
    from_account = models.ForeignKey(Account, related_name="from_account_alliance_request")
    alliance_owner = models.ForeignKey(Account, related_name="alliance_owner_account")
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred')

    def __str__(self):
        return self.from_account.username + " asking " + self.alliance_owner.username


class Message(models.Model):
    from_account = models.ForeignKey(Account, related_name="from_account_messages")
    to_account = models.ForeignKey(Account, related_name="to_account_messages")
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred')

    def __str__(self):
        return self.date_occurred + ", from " + self.from_account.username + " to " + self.to_account.username


class Badge(models.Model):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.account.username + " " + self.name


class Log(models.Model):
    city = models.ForeignKey(City)
    text = models.CharField(max_length=200)
    date_occurred = models.DateTimeField('date occurred')

    def __str__(self):
        return self.date_occurred + " " + self.text


class Cost(models.Model):
    footmen_price = models.IntegerField(default=10)
    bowmen_price = models.IntegerField(default=15)
    knights_price = models.IntegerField(default=25)
    war_machines_price = models.IntegerField(default=50)
    house_price = models.IntegerField(default=100)
    wall_price = models.IntegerField(default=1000)
    login_gold = models.IntegerField(default=100)

    def __str__(self):
        return "Cost stats"
