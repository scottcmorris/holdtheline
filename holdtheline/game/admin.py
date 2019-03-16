from django.contrib import admin
from .models import Player, Game, Flag, Card, CardLocation



admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Flag)
admin.site.register(Card)
admin.site.register(CardLocation)