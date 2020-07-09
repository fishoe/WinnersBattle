from django.db import models


# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Match(models.Model):
    winner = models.ForeignKey(Player, related_name='Winner', on_delete=models.SET_NULL, null=True, default=None)
    loser = models.ForeignKey(Player, related_name='Loser', on_delete=models.SET_NULL, null=True, default=None)
    win_hand = models.IntegerField(default=0)
    lose_hand = models.IntegerField(default=0)
    # if draw, we store p_ID in hands, and store both hand in drawHand
    draw_hand = models.IntegerField(default=0)
    pass
