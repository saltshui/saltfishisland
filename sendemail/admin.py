from django.contrib import admin
from .models import TitleRandom,AdjRandom,ContextRandom

class ContextAdmin(admin.ModelAdmin):
    list_display = ['part1','part2','part3']

# Register your models here.
admin.site.register(TitleRandom)
admin.site.register(AdjRandom)
admin.site.register(ContextRandom, ContextAdmin)
