from django.contrib import admin

# Register your models here.
from django.contrib import admin

from formation_metier.models import formation
from formation_metier.models import register
from formation_metier.models import session
from formation_metier.models import person


# Register your model here.

class RegisterInLine(admin.StackedInline):
    model = register.Register
    extra = 3


class RegisterAdmin(admin.ModelAdmin):
    fieldsets = [('session', {'fields': ['session']}),
                 ('participant', {'fields': ['participant']}),
                 ]
    list_display = ('session', 'participant', 'register_date')


class SessionAdmin(admin.ModelAdmin):
    fieldsets = [('formation', {'fields': ['formation']}),
                 ('session_date', {'fields': ['session_date']}),
                 ('local', {'fields': ['local']}),
                 ('participant_max_number', {'fields': ['participant_max_number']}),
                 ('formateur_id', {'fields': ['formateur_id']}),
                 ]
    list_display = ('formation', 'session_date', 'local', 'participant_max_number', 'formateur_id')
    inlines = [RegisterInLine]


class SessionInLine(admin.StackedInline):
    model = session.Session
    extra = 3


class FormationAdmin(admin.ModelAdmin):
    fieldsets = [('code', {'fields': ['code']}),
                 ('name', {'fields': ['name']}),
                 ('description', {'fields': ['description']})
                 ]
    inlines = [SessionInLine]
    list_display = ('name', 'code', 'description')


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [('name', {'fields': ['name']}),
                 ('numberFGS', {'fields': ['numberFGS']}),
                 ('role', {'fields': ['role']}),
                 ]
    list_display = ('name', 'numberFGS', 'role')


admin.site.register(person.Person, PersonAdmin)
admin.site.register(formation.Formation, FormationAdmin)
admin.site.register(session.Session, SessionAdmin)
admin.site.register(register.Register, RegisterAdmin)   
