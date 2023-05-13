from django.contrib import admin
from .models import Players, Answers, Questions, QuestionsRules, Event, PlayerScore

# Register your models here.

admin.site.register(Players)
admin.site.register(Answers)
admin.site.register(Questions)
admin.site.register(QuestionsRules)
admin.site.register(Event)
admin.site.register(PlayerScore)
