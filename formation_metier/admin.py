from django.contrib import admin

from formation_metier.models import formation
from formation_metier.models import register
from formation_metier.models import seance
from formation_metier.models import employe_uclouvain

admin.site.register(employe_uclouvain.EmployeUCLouvain, employe_uclouvain.EmployeUCLouvainAdmin)
admin.site.register(formation.Formation, formation.FormationAdmin)
admin.site.register(seance.Seance, seance.SeanceAdmin)
admin.site.register(register.Register, register.RegisterAdmin)
