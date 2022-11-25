from django.contrib import admin

# Register your models here.
from django.contrib import admin

from formation_metier.models import formation
from formation_metier.models import register
from formation_metier.models import seance
from formation_metier.models import person

# Register your model here.

class RegisterInLine(admin.StackedInline):
    model = register.Register
    extra = 3


class RegisterAdmin(admin.ModelAdmin):
    fieldsets = [('seance', {'fields': ['seance']}),
                 ('participant', {'fields': ['participant']}),
                 ]
    list_display = ('seance', 'participant', 'register_date')


class SeanceAdmin(admin.ModelAdmin):
    fieldsets = [('formation', {'fields': ['formation']}),
                 ('seance_date', {'fields': ['seance_date']}),
                 ('local', {'fields': ['local']}),
                 ('participant_max_number', {'fields': ['participant_max_number']}),
                 ('formateur', {'fields': ['formateur']}),
                 ('duree', {'fields': ['duree']})
                 ]
    list_display = (
        'formation', 'seance_date', 'local', 'participant_max_number', 'formateur', 'duree')
    inlines = [RegisterInLine]


class SeanceInLine(admin.StackedInline):
    model = seance.Seance
    extra = 3


class FormationAdmin(admin.ModelAdmin):
    fieldsets = [('code', {'fields': ['code']}),
                 ('name', {'fields': ['name']}),
                 ('description', {'fields': ['description']}),
                 ('public_cible', {'fields': ['public_cible']})
                 ]
    inlines = [SeanceInLine]
    list_display = ('name', 'code', 'description', 'public_cible')


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [('name', {'fields': ['name']}),
                 ('numberFGS', {'fields': ['numberFGS']}),
                 ('role_formation_metier', {'fields': ['role_formation_metier']}),
                 ('user', {'fields': ['user']}),
                 ]
    list_display = ('name', 'numberFGS', 'role_formation_metier', 'user')





admin.site.register(person.Person, PersonAdmin)
admin.site.register(formation.Formation, FormationAdmin)
admin.site.register(seance.Seance, SeanceAdmin)
admin.site.register(register.Register, RegisterAdmin)