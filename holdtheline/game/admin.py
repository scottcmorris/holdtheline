from django.contrib import admin
from .models import Player, Game, Deck, Lane, Lanes, Card


admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Lanes)
admin.site.register(Lane)
admin.site.register(Card)
admin.site.register(Deck)