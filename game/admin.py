from django.contrib import admin
from game.models import Alliance, Account, City, AllianceRequest, Message, Badge, Log, Cost, AllianceMessage, MapInfo,Map

# Register your models here.
admin.site.register(Alliance)
admin.site.register(Account)
admin.site.register(City)
admin.site.register(AllianceRequest)
admin.site.register(Message)
admin.site.register(Badge)
admin.site.register(Log)
admin.site.register(Cost)
admin.site.register(AllianceMessage)
admin.site.register(MapInfo)
admin.site.register(Map)
